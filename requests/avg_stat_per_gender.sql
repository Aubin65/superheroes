SELECT gender, alignment, COUNT(*) as nombre, ROUND(AVG(intelligence)) as avg_intelligence, ROUND(AVG(strength)) as avg_strength, ROUND(AVG(speed)) as avg_speed, ROUND(AVG(durability)) as avg_durability, ROUND(AVG(power)) as avg_power, ROUND(AVG(combat)) as avg_combat
FROM info
WHERE (gender != '-') AND (intelligence > 0) AND (alignment != '-') AND (alignment != 'neutral')
GROUP BY gender, alignment;