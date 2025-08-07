SELECT
  (
    col1 + col2 + col3 + col4 + col5 +
    col6 + col7 + col8 + col9 + col10
  ) / 10.0 AS row_mean
FROM
  parallel_big_data;