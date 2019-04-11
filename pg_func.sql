CREATE OR REPLACE FUNCTION "public"."calculate_achievement"()
  RETURNS "pg_catalog"."void" AS $BODY$BEGIN
  -- Routine body goes here...
	
	-- 删除achievewment表的数据
	-- DROP TABLE IF EXISTS "achievement";
	-- 如果结果表不存在则建立结果表
	CREATE TABLE IF NOT EXISTS "achievement" (
			ID serial PRIMARY KEY,
			salesman_name VARCHAR ( 50 ) NOT NULL,
			salesman_id INT NOT NULL,
			department_name VARCHAR ( 50 ) NOT NULL,
			department_id INT NOT NULL,
			department_line VARCHAR ( 10 ) ARRAY NOT NULL,
			order_type INT NOT NULL,
			order_money INT NOT NULL,
			order_price INT NOT NULL,
			order_date DATE NOT NULL 
	);
	CREATE INDEX IF NOT EXISTS "order_date_index" ON "achievement" (order_date);
	CREATE INDEX IF NOT EXISTS "salesmen_index" ON "achievement" (salesman_id, order_date);
	CREATE INDEX IF NOT EXISTS "order_type_index" ON "achievement" (order_type, order_date);
	
	-- 以前的数据已经固定，但是今天订单不停的新增
	
	-- 将当前日期业绩全部删除掉
	DELETE FROM "achievement" WHERE order_date=now()::DATE;
	
	-- 将结果插入到结果表中
	INSERT INTO "achievement" (salesman_name, salesman_id, department_name, department_id,
	department_line, order_type, order_money, order_price, order_date)
	SELECT
		u.real_name salesman_name,
		u.account_id salesman_id,
		d."name" department_name,
		d."id" department_id,
		STRING_TO_ARRAY( d.parent_line, '-' ) department_line,
		o.order_service_type_id order_type,
		SUM ( o.order_money ) order_money,
		SUM ( o.order_price ) order_price,
		timezone (
			'utc-8',
		to_timestamp( o.create_time )) :: DATE order_date
	FROM
		"order" AS o
		INNER JOIN "user_profile" AS u ON o.order_sales_id = u.account_id :: VARCHAR ( 20 )
		INNER JOIN "department" AS d ON u.department_id = d.ID 
	WHERE
		o.order_status = 2 
		AND o.order_valid = 1 
		AND o.order_sales_id <> '' 
		AND o.order_sales_id IS NOT NULL 
		AND u.real_name IS NOT NULL 
		AND timezone (
			'utc-8',
		to_timestamp( o.create_time ))::date = now()::date
	GROUP BY
		o.order_sales_id,
		d."id",
		d.parent_line,
		order_date,
		salesman_name,
		u.account_id,
		department_name,
		order_type
	ORDER BY
		order_Date;

END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100