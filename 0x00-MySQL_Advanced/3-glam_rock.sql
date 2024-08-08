-- Task 3: List all Glam rock bands by longevity
-- Query to list Glam rock bands by longevity
SELECT band_name, (IFNULL(split, '2022') - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;
