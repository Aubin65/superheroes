WITH color_counts AS (
    SELECT 
        "hair-color" AS color, 
        COUNT(*) AS occurrences,
        alignment
    FROM info
    WHERE "hair-color"!='-' AND alignment!='-'
    GROUP BY "hair-color", alignment
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