SELECT * FROM t_video WHERE status = 5 AND height > width AND grad_time IS NOT NULL ORDER BY RAND() @ORDER LIMIT @START,@LASTD