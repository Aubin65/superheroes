SELECT gender, ROUND(AVG("height(cm)")) as taille_moyenne, ROUND(AVG("weight(kg)")) as poids_moyen
FROM info
WHERE race='Human' 
  AND gender!='-' 
  AND ("height(cm)" BETWEEN 100 AND 300)
  AND ("weight(kg)" BETWEEN 30 AND 300)
GROUP BY gender;