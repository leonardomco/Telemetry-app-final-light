import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import math as mt
import numpy as np
from scipy.signal import savgol_filter

def donnees (annee,circuit,session,pilote) -> pd.DataFrame:


    epreuve = fastf1.get_session(annee, circuit, session)
    epreuve.load(telemetry=True, laps=True, weather=True)
    circuit_info:pd.DataFrame = epreuve.get_circuit_info()
    driver_laps = epreuve.laps.pick_drivers(pilote)
    if driver_laps.empty:
        raise ValueError(f"Aucun tour trouvé pour le pilote {pilote} dans cette session.")

    # 2. Pick the fastest lap safely
    fastest_lap = driver_laps.pick_fastest()
    if fastest_lap is None or fastest_lap.empty:
        raise ValueError(f"Le pilote {pilote} n'a enregistré aucun temps valide.")

    # 3. Safe to dropna now
    tour = fastest_lap.dropna()
    pos = tour.get_pos_data().copy()

    #tour:pd.DataFrame = epreuve.laps.pick_drivers(pilote).pick_fastest().dropna()
    #pos = tour.get_pos_data().copy()

    df_corners = circuit_info.corners
    df_corners = df_corners.loc[:, ["Number", "Distance"]]

    telemetry: pd.DataFrame = tour.get_telemetry().copy()
    

    vx = telemetry["Speed"] / 3.6
    a_scal= np.gradient(vx)
    telemetry['a_scalaire'] = a_scal
    time_float = telemetry["Time"] / np.timedelta64(1, "s")
    dtime = np.gradient(time_float)
    ax = np.gradient(vx) / dtime

    for i in np.arange(1, len(ax) - 1).astype(int):
        if ax[i] > 22.5:
            ax[i] = ax[i - 1]

    x = telemetry["X"]
    y = telemetry["Y"]
    z = telemetry["Z"]
    telemetry['Altitude'] = telemetry['Z'] - telemetry['Z'].iloc[0]

    dx = np.gradient(x)
    dy = np.gradient(y)
    dz = np.gradient(z)

    theta = np.arctan2(dy, (dx + np.finfo(float).eps))
    theta[0] = theta[1]
    theta_noDiscont = np.unwrap(theta)

    dist = telemetry["Distance"]
    ds = np.gradient(dist)
    dtheta = np.gradient(theta_noDiscont)

    # Clean up outliers
    for i in np.arange(1, len(dtheta) - 1).astype(int):
        if abs(dtheta[i]) > 0.135:
            dtheta[i] = dtheta[i - 1]

    C = dtheta / (ds + 0.0001)  
    ay = np.square(vx) * C

    for i in np.where(np.abs(ay) > 90)[0]:
        ay[i] = ay[i - 1] if i > 0 else ay[i + 1]
    
    z_theta = np.arctan2(dz, (dx + np.finfo(float).eps))
    z_theta[0] = z_theta[1]
    z_theta_noDiscont = np.unwrap(z_theta)

    z_dtheta = np.gradient(z_theta_noDiscont)

    for i in np.arange(1, len(z_dtheta) - 1).astype(int):
        if abs(z_dtheta[i]) > 0.135:
            z_dtheta[i] = z_dtheta[i - 1]

    z_C = z_dtheta / (ds + 0.0001)
    az = np.square(vx) * z_C

    for i in np.where(np.abs(az) > 120)[0]:
        az[i] = az[i - 1] if i > 0 else az[i + 1]

    a_long_smooth = savgol_filter(ax, window_length=9, polyorder=3)
    a_lat_smooth  = savgol_filter(ay, window_length=13, polyorder=3)
    az_smooth     = savgol_filter(az, window_length=21, polyorder=3)

    telemetry['vx'] = vx
    telemetry["Accélération tangentielle"] = a_long_smooth
    telemetry["Accélération normale"] = a_lat_smooth
    telemetry["Accélération verticale"] = az_smooth

    if annee < 2018 or annee > 2025:
        print ('Erreur: année non accéptée')
        return


    compound = tour['Compound']

    meteo = tour.get_weather_data().copy()
    humidité_relative = meteo["Humidity"]/100   
    presssion = meteo["Pressure"] * 100     
    temp_C = meteo["AirTemp"]
    Rs =  287.058   

    exp_term = np.exp((17.5043 * temp_C) / (241.2 + temp_C))
    rho = (1 / (Rs * (temp_C + 273.15))) * (presssion - 230.617 * humidité_relative * exp_term)
    g = 9.80665

    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    m = pd.DataFrame({
        'm_moy': [785.5, 798.0, 801.0, 807.0, 853.0, 853.0, 853.0, 855.0],
        'delta_m': [52.5, 55.0, 55.0, 55.0, 55.0, 55.0, 55.0, 55.0]
    }, index=years)

    m['m_max'] = m['m_moy'] + m['delta_m']
    m['m_min'] = m['m_moy'] - m['delta_m']


    A = 1

    c = pd.DataFrame({
        'cd_moy': [1.503],
        'cl_moy': [-3.679]
    })

    c['cd_max'] = c['cd_moy'] + 0.1 * c['cd_moy']
    c['cd_min'] = c['cd_moy'] - 0.1 * c['cd_moy']

    c['cl_max'] = c['cl_moy'] + 0.1 * c['cl_moy']
    c['cl_min'] = c['cl_moy'] - 0.1 * c['cl_moy']

    m_moy = m.loc[annee, 'm_moy']
    m_min = m.loc[annee, 'm_min']
    m_max = m.loc[annee, 'm_max']

    # pick aero coefficients
    cd_moy = c.loc[0, 'cd_moy']
    cd_min = c.loc[0, 'cd_min']
    cd_max = c.loc[0, 'cd_max']
    cl_moy = c.loc[0, 'cl_moy']
    cl_min = c.loc[0, 'cl_min']
    cl_max = c.loc[0, 'cl_max']


    telemetry['Portance_min'] = abs(0.5 * rho * (telemetry['Speed']/3.6)**2 * cl_min * A)
    telemetry['Portance_moy'] = abs(0.5 * rho * (telemetry['Speed']/3.6)**2 * cl_moy * A)
    telemetry['Portance_max'] = abs(0.5 * rho * (telemetry['Speed']/3.6)**2 * cl_max * A)

    telemetry['Trainée_min'] = 0.5 * rho * (telemetry['Speed']/3.6)**2 * cd_min * A
    telemetry['Trainée_moy'] = 0.5 * rho * (telemetry['Speed']/3.6)**2 * cd_moy * A
    telemetry['Trainée_max'] = 0.5 * rho * (telemetry['Speed']/3.6)**2 * cd_max * A

    telemetry['Force pesanteur_min'] = m_min * g
    telemetry['Force pesanteur_moy'] = m_moy * g
    telemetry['Force pesanteur_max'] = m_max * g


    P_min = abs(telemetry['Portance_min'])
    P_moy = abs(telemetry['Portance_moy'])
    P_max = abs(telemetry['Portance_max'])



    Cfr_moy = 0.015
    Cfr_min = 0.01
    Cfr_max = 0.02

    telemetry['Force de frottement de roulement min'] = (
        4 * (Cfr_min) * ((P_min + telemetry['Force pesanteur_min']) / 4)
    )

    telemetry['Force de frottement de roulement moy'] = (
        4 * (Cfr_moy) * ((P_moy + telemetry['Force pesanteur_moy']) / 4)
    )

    telemetry['Force de frottement de roulement max'] = (
        4 * (Cfr_max) * ((P_max + telemetry['Force pesanteur_max']) / 4)
    )


    brake_condition = (
        ((telemetry['Brake'] == True) | (telemetry['Accélération tangentielle'] < 0)) &
        (telemetry['Throttle'] < 5)
    )


    telemetry.loc[brake_condition, ['Force motrice max', 'Force motrice moy', 'Force motrice min']] = 0

    
    telemetry.loc[brake_condition, 'Force de freinage max'] = np.abs(
        (m_max * telemetry.loc[brake_condition, 'Accélération tangentielle']) +
        (telemetry.loc[brake_condition, 'Force de frottement de roulement min'] +
        telemetry.loc[brake_condition, 'Trainée_min'])
    )

    telemetry.loc[brake_condition, 'Force de freinage moy'] = np.abs(
        (m_moy * telemetry.loc[brake_condition, 'Accélération tangentielle']) +
        (telemetry.loc[brake_condition, 'Force de frottement de roulement moy'] +
        telemetry.loc[brake_condition, 'Trainée_moy'])
    )

    telemetry.loc[brake_condition, 'Force de freinage min'] = np.abs(
        (m_min * telemetry.loc[brake_condition, 'Accélération tangentielle']) +
        (telemetry.loc[brake_condition, 'Force de frottement de roulement min'] +
        telemetry.loc[brake_condition, 'Trainée_min'])
    )


    
    no_brake_condition = ~brake_condition


    telemetry.loc[no_brake_condition, 'Force motrice max'] = (
        (m_max * telemetry.loc[no_brake_condition, 'Accélération tangentielle']) +
        (telemetry.loc[no_brake_condition, 'Force de frottement de roulement min'] +
        telemetry.loc[no_brake_condition, 'Trainée_min'])
    )

    telemetry.loc[no_brake_condition, 'Force motrice moy'] = (
        (m_moy * telemetry.loc[no_brake_condition, 'Accélération tangentielle']) +
        (telemetry.loc[no_brake_condition, 'Force de frottement de roulement moy'] +
        telemetry.loc[no_brake_condition, 'Trainée_moy'])
    )


    telemetry.loc[no_brake_condition, 'Force motrice min'] = (
        (m_min * telemetry.loc[no_brake_condition, 'Accélération tangentielle']) +
        (telemetry.loc[no_brake_condition, 'Force de frottement de roulement max'] +
        telemetry.loc[no_brake_condition, 'Trainée_max'])
    )


    telemetry.loc[no_brake_condition, ['Force de freinage max', 'Force de freinage moy', 'Force de freinage min']] = 0


    telemetry['Force motrice max'] = telemetry['Force motrice max'].clip(lower=0)
    telemetry['Force motrice moy'] = telemetry['Force motrice moy'].clip(lower=0)
    telemetry['Force motrice min'] = telemetry['Force motrice min'].clip(lower=0)


    track = pos.loc[:, ('X', 'Y')].to_numpy()
    track_angle = circuit_info.rotation / 180 * np.pi
    def rotate(xy, *, angle):
        rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                            [-np.sin(angle), np.cos(angle)]])
        return np.matmul(xy, rot_mat)
    
    rotated_track = rotate(track, angle=track_angle)

    rotated_track = np.vstack([rotated_track, rotated_track[0]])

    
    return telemetry, rotated_track, circuit_info, df_corners

