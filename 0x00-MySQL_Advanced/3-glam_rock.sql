-- scripts lists all bands with glam rock and their main style
-- ranked by longevity
-- imports table dump called metal_bands.sql
SELECT band_name, (IFNULL(split, '2020') - IFNULL(formed, 0)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
