/*Examples SQLite commands*/

SELECT municode, CDA 
FROM TK2021_gem RIGHT JOIN general_data
ON TK2021_gem.municode = general_data.municode;

SELECT * FROM TK2021_gem INNER JOIN general_data ON
general_data.municode = TK2021_gem.municode;

SELECT *
FROM cbs_data AS c
	INNER JOIN TK2021_gem AS t1
	ON c.municode = t1.municode
	INNER JOIN TK2017_gem AS t2
	ON c.municode = t2.municode
GROUP BY c.municode;

SELECT Perioden,
 K_65Tot80Jaar_11, 
 municode 
FROM cbs_data as cbs
    INNER JOIN table_frame AS t1
    ON cbs.municode = t1.municode
WHERE Perioden = 2021
GROUP BY cbs.municode;


SELECT
	trackid,
	tracks.name AS Track,
	albums.title AS Album,
	artists.name AS Artist
FROM
	tracks
INNER JOIN albums ON albums.albumid = tracks.albumid
INNER JOIN artists ON artists.artistid = albums.artistid
WHERE
	artists.artistid = 10;