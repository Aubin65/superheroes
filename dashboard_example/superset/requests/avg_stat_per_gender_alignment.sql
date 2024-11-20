SELECT gender, alignment, 'intelligence' AS attribute, ROUND(AVG(intelligence)) AS avg_value
FROM info
WHERE gender != '-' AND intelligence > 0 AND alignment != '-' AND alignment != 'neutral'
GROUP BY gender, alignment

UNION ALL

SELECT gender, alignment, 'strength' AS attribute, ROUND(AVG(strength)) AS avg_value
FROM info
WHERE gender != '-' AND intelligence > 0 AND alignment != '-' AND alignment != 'neutral'
GROUP BY gender, alignment

UNION ALL

SELECT gender, alignment, 'speed' AS attribute, ROUND(AVG(speed)) AS avg_value
FROM info
WHERE gender != '-' AND intelligence > 0 AND alignment != '-' AND alignment != 'neutral'
GROUP BY gender, alignment

UNION ALL

SELECT gender, alignment, 'durability' AS attribute, ROUND(AVG(durability)) AS avg_value
FROM info
WHERE gender != '-' AND intelligence > 0 AND alignment != '-' AND alignment != 'neutral'
GROUP BY gender, alignment

UNION ALL

SELECT gender, alignment, 'power' AS attribute, ROUND(AVG(power)) AS avg_value
FROM info
WHERE gender != '-' AND intelligence > 0 AND alignment != '-' AND alignment != 'neutral'
GROUP BY gender, alignment

UNION ALL

SELECT gender, alignment, 'combat' AS attribute, ROUND(AVG(combat)) AS avg_value
FROM info
WHERE gender != '-' AND intelligence > 0 AND alignment != '-' AND alignment != 'neutral'
GROUP BY gender, alignment;
