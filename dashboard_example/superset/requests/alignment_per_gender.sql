SELECT gender, alignment, COUNT(*) as nombre
FROM info
WHERE (gender != '-') AND (alignment != '-')
GROUP BY gender, alignment;