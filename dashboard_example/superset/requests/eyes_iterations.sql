WITH color_counts AS (
    SELECT 
        "eye-color" AS color, 
        COUNT(*) AS occurrences,
        alignment
    FROM info
    WHERE "eye-color"!='-' AND alignment!='-'
    GROUP BY "eye-color", alignment
)
SELECT 
    CASE 
        WHEN occurrences >= 10 THEN color
        ELSE 'Autre'
    END AS grouped_color,
    SUM(occurrences) AS total_occurrences,
    alignment
FROM color_counts
GROUP BY 
    CASE 
        WHEN occurrences >= 10 THEN color
        ELSE 'Autre'
    END,
    alignment;
