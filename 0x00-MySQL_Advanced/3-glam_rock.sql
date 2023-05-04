-- scripts lists all bands with glam rock and their main style
-- ranked by longevity
-- imports table dump called metal_bands.sql
SELECT band_name,
CASE
    WHEN split IS NULL then (2020 - formed)
    ELSE split - formed
END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
