-- Nombre total d'accidents par année
SELECT an, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY an
ORDER BY an;

-- Liste des accidents avec blessures graves
SELECT c.Num_Acc, c.jour, c.mois, c.an, c.adresse
FROM caractèristiques c
JOIN usagers u ON c.Num_Acc = u.Num_Acc
WHERE u.gravité_blessure = 3
GROUP BY c.Num_Acc;

-- Répartition des accidents par conditions atmosphériques
SELECT cond_atmosphériques, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY cond_atmosphériques
ORDER BY nombre_accidents DESC;

-- Accidents impliquant des piétons
SELECT c.Num_Acc, c.jour, c.mois, c.an, c.adresse
FROM caractèristiques c
JOIN usagers u ON c.Num_Acc = u.Num_Acc
WHERE u.catégorie_usager = 1
GROUP BY c.Num_Acc;

-- Distribution des accidents par luminosité
SELECT luminosité, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY luminosité
ORDER BY nombre_accidents DESC;

-- Accidents par département, classés par fréquence
SELECT departement, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY departement
ORDER BY nombre_accidents DESC;

-- Accidents impliquant des véhicules électriques
SELECT c.Num_Acc, c.jour, c.mois, c.an
FROM caractèristiques c
JOIN vehicule v ON c.Num_Acc = v.Num_Acc
WHERE v.motorisation = 5
GROUP BY c.Num_Acc;

-- Nombre d'accidents par type de collision
SELECT type_de_collision, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY type_de_collision
ORDER BY nombre_accidents DESC;

-- Répartition des accidents par état de surface
SELECT l.etat_surface, COUNT(*) AS nombre_accidents
FROM lieux l
GROUP BY l.etat_surface
ORDER BY nombre_accidents DESC;

-- Accidents par catégorie de véhicule impliqué
SELECT v.catégorie_vehicule, COUNT(DISTINCT c.Num_Acc) AS nombre_accidents
FROM caractèristiques c
JOIN vehicule v ON c.Num_Acc = v.Num_Acc
GROUP BY v.catégorie_vehicule
ORDER BY nombre_accidents DESC;

-- Nombre d'usagers par sexe impliqués dans des accidents
SELECT sexe, COUNT(*) AS nombre_usagers
FROM usagers
GROUP BY sexe;

-- Accidents par heure de la journée
SELECT SUBSTR(heure, 1, 2) AS heure_jour, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY heure_jour
ORDER BY heure_jour;

-- Accidents par jour de la semaine
SELECT jour, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY jour
ORDER BY jour;

-- Âge moyen des usagers impliqués dans les accidents
SELECT c.an - u.année_naissance AS age, COUNT(*) AS nombre_usagers
FROM usagers u
JOIN caractèristiques c ON u.Num_Acc = c.Num_Acc
WHERE u.année_naissance > 0
GROUP BY age
ORDER BY age;

-- Accidents en fonction du type de trajet
SELECT u.trajet, COUNT(DISTINCT c.Num_Acc) AS nombre_accidents
FROM caractèristiques c
JOIN usagers u ON c.Num_Acc = u.Num_Acc
GROUP BY u.trajet
ORDER BY nombre_accidents DESC;

-- Accidents en agglomération vs hors agglomération
SELECT agglomération, COUNT(*) AS nombre_accidents
FROM caractèristiques
GROUP BY agglomération;

-- Gravité des blessures par catégorie d'usager
SELECT catégorie_usager, gravité_blessure, COUNT(*) AS nombre_usagers
FROM usagers
GROUP BY catégorie_usager, gravité_blessure
ORDER BY catégorie_usager, gravité_blessure;

-- Accidents en fonction du régime de circulation
SELECT l.régime_circulation, COUNT(*) AS nombre_accidents
FROM lieux l
GROUP BY l.régime_circulation
ORDER BY nombre_accidents DESC;

-- Localisation géographique des accidents les plus graves
SELECT c.latitude, c.longitude, c.adresse
FROM caractèristiques c
JOIN usagers u ON c.Num_Acc = u.Num_Acc
WHERE u.gravité_blessure >= 3
GROUP BY c.Num_Acc
HAVING COUNT(*) > 0;

-- Utilisation des équipements de sécurité par gravité de blessure
SELECT u.secu_1, u.gravité_blessure, COUNT(*) AS nombre_usagers
FROM usagers u
WHERE u.secu_1 IS NOT NULL
GROUP BY u.secu_1, u.gravité_blessure
ORDER BY u.secu_1, u.gravité_blessure;