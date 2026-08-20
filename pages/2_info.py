import streamlit as st
import pandas as pd

lang = st.session_state.lang

# --------------------------------------------------
# Translations
# --------------------------------------------------
TEXT = {
    "Français": {
        "title": "Informations concernant les données présentées",
        "toc": "Table des matières",

        "phys": "Grandeurs physiques",
        "trajectory": "Trajectoire",
        "trajectory_1": "La trajectoire est l’ensemble des positions occupées par la voiture de Formule 1 au cours du temps.",
        "trajectory_2": "Dans le plan, elle est représentée par la courbe d’équation $y(x)$.",

        "altitude": "Altitude",
        "altitude_1": "L'altitude est représentée en prenant le premier point comme point de référence.",
        "altitude_2": "Elle est décrite par la fonction $altitude(s)$, où $s$ représente la distance parcourue.",

        "speed": "Vitesse",
        "speed_1": "La vitesse présentée est la norme du vecteur vitesse en fonction de la distance parcourue.",
        "speed_2": "Le vecteur vitesse est obtenu par dérivation du vecteur position.",

        "tan_acc": "Accélération tangentielle",
        "tan_acc_1": "L’accélération tangentielle est la composante de l’accélération dont la direction est tangente à la trajectoire.",
        "tan_acc_2": "Elle est définie comme la variation de la norme de la vitesse par unité de temps :",
        "tan_acc_3": "Dans les graphiques présentés, l’accélération tangentielle est représentée en fonction de la distance parcourue $s$.",

        "norm_acc": "Accélération normale",
        "norm_acc_1": "L’accélération normale est la composante de l’accélération dont la direction est orthogonale à la trajectoire.",
        "norm_acc_2": "Elle est définie comme le produit entre le carré de la vitesse et la courbure :",
        "norm_acc_3": "La courbure peut être définie comme la valeur absolue de la variation de l’angle $\\theta$ par rapport à la distance parcourue $s$ :",
        "norm_acc_4": "Dans le cas d’une trajectoire plane décrite par une fonction $y(x)$, l’angle $\\theta$ entre la tangente et l’axe $x$ vérifie :",
        "norm_acc_5": "Dans les graphiques présentés, l’accélération normale est représentée en fonction de la distance parcourue $s$.",

        "vert_acc": "Accélération verticale",
        "vert_acc_1": "L’accélération verticale est la composante de l’accélération suivant l’axe vertical.",
        "vert_acc_2": "Elle est définie de façon analogue à l'accélération normale mais dans le plan $Oxz$.",
        "vert_acc_3": "Il est donc possible de définir la courbure verticale comme :",
        "vert_acc_4": "Dans le cas d’une trajectoire sur le plan $Oxz$ décrite par une fonction $z(x)$, l’angle $\\theta_z$ entre la tangente et l’axe $x$ vérifie :",
        "vert_acc_5": "L'accélération verticale est donc définie comme :",
        "vert_acc_6": "Dans les graphiques présentés, cette accélération est représentée en fonction de la distance parcourue $s$.",

        "lift": "Portance",
        "lift_1": "La portance est la composante de la force aérodynamique qui s’exerce perpendiculairement à la vitesse relative de l’air autour du véhicule.",
        "lift_2": "La norme de cette force est donnée par :",
        "lift_3": "Dans cette expression, $\\rho$ est la densité de l’air, $A$ l’aire de référence aérodynamique, $C_L$ le coefficient de portance et $v$ la norme de la vitesse.",
        "lift_4": "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$.",

        "drag": "Traînée",
        "drag_1": "La traînée est la force qui s’oppose au mouvement de la voiture dans l’air.",
        "drag_2": "La norme de cette force est définie par :",
        "drag_3": "Dans cette expression, $\\rho$ est la densité de l’air, $A$ l’aire frontale, $C_D$ le coefficient de traînée et $v$ la norme de la vitesse.",
        "drag_4": "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$.",

        "fr": "Force de frottement de roulement",
        "fr_1": "Il s'agit de la force de frottement due au contact entre les pneus de la voiture et la surface.",
        "fr_2": "Dans ma modélisation, nous allons supposer que ces roues sont des roues libres c’est-à-dire non freinées, ce qui est une simplification.",
        "fr_3": "La norme de cette force est définie par :",
        "fr_4": "Dans cette expression, $F_s$ est la force de soutien qui est la somme de la portance et de la force de pesanteur.",
        "fr_5": "$C_{fr}$ est quant à lui le coefficient de frottement au roulement.",

        "motrice": "Force motrice",
        "motrice_1": "La force motrice est la force résultant de l'action du moteur qui permet à la voiture de se déplacer dans le sens du mouvement.",
        "motrice_2": "Elle est définie à partir du principe fondamental de la dynamique appliqué au véhicule lorsqu'il accélère sans freiner.",
        "motrice_3": "La norme de cette force est définie par :",
        "motrice_4": "Dans cette expression, $m$ représente la masse du véhicule et $a_t$ son accélération longitudinale.",
        "motrice_5": "$F_r$ correspond à la force de frottement de roulement tandis que $F_D$ représente la force de traînée aérodynamique.",
        "motrice_6": "La force motrice n'est appliquée que lorsque le véhicule accélère et qu'aucune force de freinage n'est exercée.",

        "freinage": "Force de freinage",
        "freinage_1": "La force de freinage est la force opposée au sens du déplacement qui permet au véhicule de diminuer sa vitesse.",
        "freinage_2": "Cette force dépend de l'action des freins et est définie à partir du principe fondamental de la dynamique appliqué au véhicule lorsqu'il est en phase de décélération.",
        "freinage_3": "La norme de cette force est définie par :",
        "freinage_4": "Dans cette expression, $m$ représente la masse du véhicule et $a_t$ son accélération longitudinale.",
        "freinage_5": "$F_D$ correspond à la force de traînée aérodynamique tandis que $F_r$ représente la force de frottement de roulement.",
        "freinage_6": "La force de freinage est opposée au mouvement du véhicule.",
        "freinage_7": "La force de freinage n'est appliquée que lorsque le véhicule décélère et que les freins sont actionnés.",
        "freinage_8": "Lorsque le véhicule accélère ou qu'aucune action de freinage n'est exercée, la force de freinage est considérée comme nulle.",

        },

    "English": {
        "title": "Information concerning the presented data",
        "toc": "Table of contents",

        "phys": "Physical quantities",
        "trajectory": "Trajectory",
        "trajectory_1": "The trajectory is the set of positions occupied by the Formula 1 car over time.",
        "trajectory_2": "In the plane, it is represented by the curve of equation $y(x)$.",

        "altitude": "Altitude",
        "altitude_1": "The altitude is represented by taking the first point as the reference point.",
        "altitude_2": "It is described by the function $altitude(s)$, where $s$ represents the traveled distance.",

        "speed": "Speed",
        "speed_1": "The presented speed is the norm of the velocity vector as a function of the traveled distance.",
        "speed_2": "The velocity vector is obtained by differentiation of the position vector.",

        "tan_acc": "Tangential acceleration",
        "tan_acc_1": "Tangential acceleration is the component of acceleration whose direction is tangent to the trajectory.",
        "tan_acc_2": "It is defined as the variation of the norm of the speed per unit of time:",
        "tan_acc_3": "In the presented graphs, tangential acceleration is represented as a function of the traveled distance $s$.",

        "norm_acc": "Normal acceleration",
        "norm_acc_1": "Normal acceleration is the component of acceleration whose direction is orthogonal to the trajectory.",
        "norm_acc_2": "It is defined as the product between the square of the speed and the curvature:",
        "norm_acc_3": "The curvature can be defined as the absolute value of the variation of the angle $\\theta$ with respect to the traveled distance $s$:",
        "norm_acc_4": "In the case of a planar trajectory described by a function $y(x)$, the angle $\\theta$ between the tangent and the $x$ axis satisfies:",
        "norm_acc_5": "In the presented graphs, normal acceleration is represented as a function of the traveled distance $s$.",

        "vert_acc": "Vertical acceleration",
        "vert_acc_1": "Vertical acceleration is the component of acceleration along the vertical axis.",
        "vert_acc_2": "It is defined in a similar way to normal acceleration but in the $Oxz$ plane.",
        "vert_acc_3": "It is therefore possible to define the vertical curvature as:",
        "vert_acc_4": "In the case of a trajectory in the $Oxz$ plane described by a function $z(x)$, the angle $\\theta_z$ between the tangent and the $x$ axis satisfies:",
        "vert_acc_5": "Vertical acceleration is therefore defined as:",
        "vert_acc_6": "In the presented graphs, this acceleration is represented as a function of the traveled distance $s$.",

        "lift": "Lift",
        "lift_1": "Lift is the component of the aerodynamic force that acts perpendicularly to the relative air velocity around the vehicle.",
        "lift_2": "The norm of this force is given by:",
        "lift_3": "In this expression, $\\rho$ is the air density, $A$ the aerodynamic reference area, $C_L$ the lift coefficient and $v$ the norm of the speed.",
        "lift_4": "In the presented graphs, its norm is displayed as a function of the traveled distance $s$.",

        "drag": "Drag",
        "drag_1": "Drag is the force that opposes the movement of the car through the air.",
        "drag_2": "The norm of this force is defined by:",
        "drag_3": "In this expression, $\\rho$ is the air density, $A$ the frontal area, $C_D$ the drag coefficient and $v$ the norm of the speed.",
        "drag_4": "In the presented graphs, its norm is displayed as a function of the traveled distance $s$.",

        "fr": "Rolling resistance force",
        "fr_1": "This is the friction force caused by the contact between the vehicle's tires and the road surface.",
        "fr_2": "In my model, I will assume that these wheels are free-rolling wheels, meaning they are not braked, which is a simplification.",
        "fr_3": "The magnitude of this force is defined as:",
        "fr_4": "In this expression, $F_s$ is the normal force, which is the sum of the lift force and the gravitational force.",
        "fr_5": "$C_{fr}$ is the rolling resistance coefficient.",

        "motrice": "Traction force",
        "motrice_1": "The traction force is the force generated by the engine that enables the vehicle to move in the direction of travel.",
        "motrice_2": "It is defined using Newton's second law applied to the vehicle when it is accelerating without braking.",
        "motrice_3": "The magnitude of this force is defined as:",
        "motrice_4": "In this expression, $m$ represents the vehicle mass and $a_t$ its longitudinal acceleration.",
        "motrice_5": "$F_r$ corresponds to the rolling resistance force, while $F_D$ represents the aerodynamic drag force.",
        "motrice_6": "The traction force is applied only when the vehicle is accelerating and no braking force is exerted.",

        "freinage": "Braking force",
        "freinage_1": "The braking force is the force acting opposite to the direction of motion that enables the vehicle to reduce its speed.",
        "freinage_2": "This force depends on the action of the brakes and is defined using Newton's second law applied to the vehicle during deceleration.",
        "freinage_3": "The magnitude of this force is defined as:",
        "freinage_4": "In this expression, $m$ represents the vehicle mass and $a_t$ its longitudinal acceleration.",
        "freinage_5": "$F_D$ corresponds to the aerodynamic drag force, while $F_r$ represents the rolling resistance force.",
        "freinage_6": "The braking force acts opposite to the vehicle's motion.",
        "freinage_7": "The braking force is applied only when the vehicle is decelerating and the brakes are engaged.",
        "freinage_8": "When the vehicle is accelerating or no braking action is applied, the braking force is considered to be zero.",


    }
}

TEXT["Français"].update({
    "approx": "Approximations réalisées",
    "approx_intro": "Dans ce travail, plusieurs hypothèses ont dû être réalisées afin de rendre les calculs possibles.",

    "approx_point": "Approximation ponctuelle",
    "approx_point_txt": (
        "Le véhicule est assimilé à un point, ce qui permet de négliger les moments "
        "de force, d’inertie et cinétique ainsi que les transferts de charge. Cela permet également "
        "d’appliquer le principe fondamental de la dynamique."
    ),

    "approx_mass": "Masse supposées constante",
    "approx_mass_txt": (
        "La masse est considérée constante dans le temps alors qu’elle diminue normalement à mesure que le "
        "carburant est utilisé. Cette hypothèse est nécessaire puisque la variation de masse du carburant n’est pas connue."
    ),

    "approx_vert": "Accélération verticale supposées nulle dans la partie dynamique",
    "approx_vert_txt": (
        "Cette approximation se justifie par le fait que l’accélération verticale dépend principalement des variations ponctuelles "
        "de la surface de roulage. En règle générale, elle peut donc être approximée à 0 en dehors de ces irrégularités."
    ),

    "approx_wheels": "Roues supposées libres",
    "approx_wheels_txt": (
        "Cette hypothèse est valable la majeure partie du temps, lorsque les voitures ne freinent pas, et simplifie la "
        "modélisation de la force de frottement de roulement."
    ),

    "approx_engine": "Force motrice supposée nulle lors des freinages",
    "approx_engine_txt": (
        "Cela revient à négliger le frein moteur, car il n’est pas possible de le quantifier."
    ),
})

TEXT["English"].update({
    "approx": "Performed approximations",
    "approx_intro": "In this work, several assumptions had to be made in order to make the calculations possible.",

    "approx_point": "Point approximation",
    "approx_point_txt": (
        "The vehicle is assimilated to a point, which makes it possible to neglect force moments, inertia and kinetic "
        "effects as well as load transfers. This also makes it possible to apply the fundamental principle of dynamics."
    ),

    "approx_mass": "Mass assumed constant",
    "approx_mass_txt": (
        "The mass is considered constant over time whereas it normally decreases as fuel is used. "
        "This assumption is necessary since the variation of the fuel mass is not known."
    ),

    "approx_vert": "Vertical acceleration assumed zero in the dynamic part",
    "approx_vert_txt": (
        "This approximation is justified by the fact that vertical acceleration mainly depends on punctual variations "
        "of the rolling surface. In general, it can therefore be approximated to 0 outside these irregularities."
    ),

    "approx_wheels": "Wheels assumed free",
    "approx_wheels_txt": (
        "This assumption is valid most of the time, when cars are not braking, and simplifies the "
        "modeling of rolling resistance force."
    ),

    "approx_engine": "Driving force assumed zero during braking",
    "approx_engine_txt": (
        "This amounts to neglecting engine braking, since it is not possible to quantify it."
    ),
})

TEXT["Français"].update({
    "coeff": "Estimations des coefficients et leur limites",

    "mass_cars": "Masse des voitures",
    "mass_cars_txt": "La masse des voitures est calculée à l'aide de la formule suivante :",
    "mass_cars_txt2": "La masse est considérée la même pour toute les voitures et dépend simplement de l'année. Ainsi voici la masse en fonction des années :",
    "mass_note": "Les masses minimales sont définies par les règlements FIA",

    "air_density": "Masse volumique de l'air",
    "air_density_txt": (
        "La masse volumique de l’air $\\rho$ est définie à l’aide d’une formule empirique "
        "qui l’exprime en fonction de la pression $p$, de la température $T$ "
        "et de l’humidité relative $h$ :"
    ),

    "aero": "Coefficients aérodynamiques",
    "aero_txt": (
        "Les coeffcients aerodynamiques proviennent de plusieurs sources sur internet. "
        "Les valeurs sont les mêmes pour toutes les voitures même si cela ne devrait pas être le cas. Voici les valeurs : "
    ),

    "roll": "Coefficient de frottement de roulement",
    "roll_txt1": "Pour le coefficient de frottement de roulement il faut également l'estimer à l'aide de valeurs présentent dans la littérature. ",
    "roll_txt2": "Souvent les valeurs présentées sur internet se situent entre 0,01 et 0,02 je vais donc garder la valeur centrale :",

    "uncert": "Incertitudes",
    "uncert_txt": "Les coefficients impliquent une incértitude puisqu'ils sont estimés.",
    "uncert_txt2": "Pour la masse cela est détaillé plus haut.",
    "uncert_txt3": "Pour la masse volumique de l'air je ne vais pas considérer d'incertitude car les données atmosphériques sont précises",
    "uncert_txt4": "Pour les coeffcients aérodynamiques, je vais considérer une incertitude de 10%",
    "uncert_txt5": "Pour le coefficient de frottement de roulement je vais considérer les valeurs maximales et minimales trouvées pour l'incertitude.",
    "uncert_txt6": "Les incertitudes sont présentées sur les graphiques par la zone de couleur ombrée.",
})

TEXT["English"].update({
    "coeff": "Estimation of coefficients and their limits",

    "mass_cars": "Car mass",
    "mass_cars_txt": "The mass of the cars is calculated using the following formula:",
    "mass_cars_txt2": "The mass is considered the same for all cars and depends only on the year. Thus here is the mass as a function of the years:",
    "mass_note": "Minimum masses are defined by FIA regulations",

    "air_density": "Air density",
    "air_density_txt": (
        "Air density $\\rho$ is defined using an empirical formula "
        "which expresses it as a function of pressure $p$, temperature $T$ "
        "and relative humidity $h$:"
    ),

    "aero": "Aerodynamic coefficients",
    "aero_txt": (
        "Aerodynamic coefficients come from several sources on the internet. "
        "The values are the same for all cars even though this should not be the case. Here are the values:"
    ),

    "roll": "Rolling resistance coefficient",
    "roll_txt1": "For the rolling resistance coefficient it must also be estimated using values found in the literature.",
    "roll_txt2": "Often the values presented on the internet are between 0.01 and 0.02 so I will therefore keep the central value:",

    "uncert": "Uncertainties",
    "uncert_txt": "The coefficients involve an uncertainty since they are estimated.",
    "uncert_txt2": "For the mass this is detailed above.",
    "uncert_txt3": "For air density I will not consider uncertainty because atmospheric data are precise",
    "uncert_txt4": "For aerodynamic coefficients, I will consider a 10% uncertainty",
    "uncert_txt5": "For the rolling resistance coefficient I will consider the maximum and minimum values found for the uncertainty.",
    "uncert_txt6": "Uncertainties are presented on the graphs by the shaded colored area.",
})

TEXT["Français"].update({
    "processing": "Traitement des données",
    "processing_txt1": "Les graphiques des trois accélérations sont traités afin de les rendre lisibles et de supprimer le bruit.",
    "processing_txt2": (
        "Le traitement de ces données repose sur un algorithme combinant la substitution des valeurs extrêmes "
        "par les valeurs précédentes et un filtrage de Savitzky–Golay."
    ),
    "processing_param": "Paramètrage du traitement des données",
})

TEXT["English"].update({
    "processing": "Data processing",
    "processing_txt1": "The graphs of the three accelerations are processed in order to make them readable and to remove noise.",
    "processing_txt2": (
        "The processing of these data relies on an algorithm combining the substitution of extreme values "
        "by previous values and Savitzky–Golay filtering."
    ),
    "processing_param": "Data processing parameters",
})


TEXT["Français"].update({
    "sg_filter": "- Filtre de Savitzky–Golay :",
    "angle_outliers": "- Suppression des valeurs aberrantes des angles (pour $a_n$ et $a_v$) :",
    "acc_outliers": "- Suppression des valeurs aberrantes des accélérations :",
})

TEXT["English"].update({
    "sg_filter": "- Savitzky–Golay filter:",
    "angle_outliers": "- Removal of outlier angle values (for $a_n$ and $a_v$):",
    "acc_outliers": "- Removal of acceleration outliers:",
})
TEXT["Français"].update({
    "for_at": "pour $a_t$",
    "for_an": "pour $a_n$",
    "for_av": "pour $a_v$",
})

TEXT["English"].update({
    "for_at": "for $a_t$",
    "for_an": "for $a_n$",
    "for_av": "for $a_v$",
})

def t(key):
    return TEXT[lang][key]

# --------------------------------------------------
# Page content
# --------------------------------------------------
st.title(t("title"))

st.markdown(f"## {t('toc')}")
st.markdown(f"""
- [1. {t("phys")}](#1-{t("phys").lower().replace(" ", "-")})
- [2. {t("approx")}](#2-{t("approx").lower().replace(" ", "-")})
- [3. {t("coeff")}](#3-{t("coeff").lower().replace(" ", "-")})
- [4. {t("processing")}](#4-{t("processing").lower().replace(" ", "-")})
""")

st.markdown(f"## 1. {t('phys')}")

st.subheader(t("trajectory"))
st.write(t("trajectory_1"))
st.write(t("trajectory_2"))

st.subheader(t("altitude"))
st.write(t("altitude_1"))
st.write(t("altitude_2"))

st.subheader(t("speed"))
st.write(t("speed_1"))
st.latex(r"\lVert \vec{v}(s) \rVert")
st.write(t("speed_2"))

st.subheader(t("tan_acc"))
st.write(t("tan_acc_1"))
st.write(t("tan_acc_2"))
st.latex(r"a_{\mathrm{t}}(t) = \frac{dv(t)}{dt}")
st.write(t("tan_acc_3"))

st.subheader(t("norm_acc"))
st.write(t("norm_acc_1"))
st.write(t("norm_acc_2"))
st.latex(r"a_{\mathrm{n}}(t) = v(t)^2\,\gamma")
st.write(t("norm_acc_3"))
st.latex(r"\gamma = \left\lvert \frac{d\theta}{ds} \right\rvert")
st.write(t("norm_acc_4"))
st.latex(r"\theta = \arctan\!\left(\frac{dy}{dx}\right)")
st.write(t("norm_acc_5"))

st.subheader(t("vert_acc"))
st.write(t("vert_acc_1"))
st.write(t("vert_acc_2"))
st.write(t("vert_acc_3"))
st.latex(r"\gamma_z = \left\lvert \frac{d\theta_z}{ds_z} \right\rvert")
st.write(t("vert_acc_4"))
st.latex(r"\theta_z = \arctan\!\left(\frac{dz}{dx}\right)")
st.write(t("vert_acc_5"))
st.latex(r"a_{\mathrm{v}}(t) = v(t)^2\,\gamma_z")
st.write(t("vert_acc_6"))

st.subheader(t("lift"))
st.write(t("lift_1"))
st.write(t("lift_2"))
st.latex(r"\lVert \vec{F}_L(t) \rVert = \frac{1}{2}\,\rho\,v(t)^2\,A\,C_L")
st.write(t("lift_3"))
st.write(t("lift_4"))

st.subheader(t("drag"))
st.write(t("drag_1"))
st.write(t("drag_2"))
st.latex(r"\lVert \vec{F}_D(t) \rVert = \frac{1}{2}\,\rho\,v(t)^2\,A\,C_D")
st.write(t("drag_3"))
st.write(t("drag_4"))

st.subheader(t("fr"))
st.write(t("fr_1"))
st.write(t("fr_2"))
st.write(t("fr_3"))
st.latex(r"\lVert \vec{F}_r(t) \rVert = C_{fr}\,F_s(t)")
st.write(t("fr_4"))
st.write(t("fr_5"))

st.subheader(t("motrice"))
st.write(t("motrice_1"))
st.write(t("motrice_2"))
st.write(t("motrice_3"))
if lang == "Français":
    st.latex(r"""
    \left\lVert \vec{F}_{m}(t) \right\rVert =
    \begin{cases}
    m\,a_t(t) + F_r(t) + F_D(t),
    & \text{si } a_t > 0 \text{ et que la voiture ne freine pas} \\[6pt]
    0,
    & \text{si } a_t < 0 \text{ et que la voiture freine}
    \end{cases}
    """)
else:
    st.latex(r"""
    \left\lVert \vec{F}_{m}(t) \right\rVert =
    \begin{cases}
    m\,a_t(t) + F_r(t) + F_D(t),
    & \text{si } a_t > 0 \text{ and the car is not braking} \\[6pt]
    0,
    & \text{si } a_t < 0 \text{ and the car is braking}
    \end{cases}
    """)
st.write(t("motrice_4"))
st.write(t("motrice_5"))
st.write(t("motrice_6"))

st.subheader(t("freinage"))
st.write(t("freinage_1"))
st.write(t("freinage_2"))
st.write(t("freinage_3"))
if lang == "Français":
    st.latex(r"""
    \left\lVert \vec{F}_{freins}(t) \right\rVert =
    \begin{cases}
    m\,|a_t(t)| + |F_D(t)| + |F_r(t)|,
    & \text{si } a_t < 0 \text{ et que la voiture freine} \\[6pt]
    0,
    & \text{si } a_t > 0 \text{ et que la voiture ne freine pas}
    \end{cases}
    """)
else:
    st.latex(r"""
    \left\lVert \vec{F}_{brakes}(t) \right\rVert =
    \begin{cases}
    m\,|a_t(t)| + |F_D(t)| + |F_r(t)|,
    & \text{if } a_t < 0 \text{ and the car is braking} \\[6pt]
    0,
    & \text{if } a_t > 0 \text{ and the car is not braking}
    \end{cases}
    """)
st.write(t("freinage_4"))
st.write(t("freinage_5"))
st.write(t("freinage_6"))
st.write(t("freinage_7"))


st.markdown(f"## 2. {t('approx')}")
st.write(t("approx_intro"))

st.subheader(t("approx_point"))
st.write(t("approx_point_txt"))

st.subheader(t("approx_mass"))
st.write(t("approx_mass_txt"))

st.subheader(t("approx_vert"))
st.write(t("approx_vert_txt"))

st.subheader(t("approx_wheels"))
st.write(t("approx_wheels_txt"))

st.subheader(t("approx_engine"))
st.write(t("approx_engine_txt"))

data = {
    "Année": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "Masse minimale de la voiture (kg)": [733, 743, 746, 752, 798, 798, 798, 800],
    "Masse maximale de carburant (kg)": [105, 110, 110, 110, 110, 110, 110, 110],
    "Masse totale (kg)": [
        "785.5 ± 52.5",
        "798 ± 55",
        "801 ± 55",
        "807 ± 55",
        "853 ± 55",
        "853 ± 55",
        "853 ± 55",
        "855 ± 55",
    ],
}

df = pd.DataFrame(data)

df_display = df.copy()
if lang == "English":
    df_display.columns = [
        "Year",
        "Minimum car mass (kg)",
        "Maximum fuel mass (kg)",
        "Total mass (kg)",
    ]





st.markdown(f"## 3. {t('coeff')}")

st.subheader(t("mass_cars"))
st.write(t("mass_cars_txt"))
st.latex(r"m = m_{min\; voiture} + \frac{1}{2} m_{max\; carburant} \pm \frac{1}{2} m_{max\; carburant}")
st.write(t("mass_cars_txt2"))

st.table(df_display)
st.write(t("mass_note"))

st.subheader(t("air_density"))
st.write(t("air_density_txt"))
st.latex(r"\rho(h, T, p) = \frac{1}{R_s(T + 273,15)}\bigg(p-230,617 \cdot h\cdot e^{\Big(\frac{17,5043T}{241,2 + T}\Big)}\bigg)")

st.subheader(t("aero"))
st.write(t("aero_txt"))
st.write("$C_D$ = 1,503")
st.write("$C_L$ = -3,679")
st.write("$A$ = 1 $m^2$")

st.subheader(t("roll"))
st.write(t("roll_txt1"))
st.write(t("roll_txt2"))
st.latex(r"C_{fr}= 0,015")

st.subheader(t("uncert"))
st.write(t("uncert_txt"))
st.write(t("uncert_txt2"))
st.write(t("uncert_txt3"))
st.write(t("uncert_txt4"))
st.write(t("uncert_txt5"))
st.write(t("uncert_txt6"))




st.markdown(f"## 4. {t('processing')}")
st.write(t("processing_txt1"))
st.write(t("processing_txt2"))

st.subheader(t("processing_param"))

st.write(t("sg_filter"))
if lang == "Français":
    st.latex(r"""
    \begin{aligned}
    &\text{window\_length} = 9 \quad \text{pour } a_t \\
    &\text{window\_length} = 13 \quad \text{pour } a_n \\
    &\text{window\_length} = 21 \quad \text{pour } a_v \\
    &\text{polyorder} = 3
    \end{aligned}
    """)
else:
    st.latex(r"""
    \begin{aligned}
    &\text{window\_length} = 9 \quad \text{for } a_t \\
    &\text{window\_length} = 13 \quad \text{for } a_n \\
    &\text{window\_length} = 21 \quad \text{for } a_v \\
    &\text{polyorder} = 3
    \end{aligned}
    """)

st.write(t("angle_outliers"))
st.latex(r"d\theta[i] > 0.135~\mathrm{rad} \;\Rightarrow\; d\theta[i] = d\theta[i-1]")
st.latex(r"d\theta_z[i] > 0.135~\mathrm{rad} \;\Rightarrow\; d\theta_z[i] = d\theta_z[i-1]")

st.write(t("acc_outliers"))
st.latex(r"a_t[i] > 22.5 \;\Rightarrow\; a_t[i] = a_t[i-1]")
st.latex(r"\lvert a_n[i] \rvert > 90 \;\Rightarrow\; a_n[i] = a_n[i-1]")
st.latex(r"\lvert a_v[i] \rvert > 120 \;\Rightarrow\; a_v[i] = a_v[i-1]")
