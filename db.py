

def setup():
  # with connection:
    with connection.cursor() as cursor:

      cursor.execute("""CREATE TABLE IF NOT EXISTS `user` (
        `id` int NOT NULL AUTO_INCREMENT,
        `email` varchar(255) NOT NULL,
        `username` varchar(255) NOT NULL,
        `password` varchar(255) NOT NULL,
        `name` varchar(255) NOT NULL,
        `age` int NOT NULL,
        `height` int NOT NULL,
        `weight` int NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `username` (`username`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `product` (
        `id` int NOT NULL AUTO_INCREMENT,
        `product_name` varchar(255) DEFAULT NULL,
        `rating` int DEFAULT NULL,
        `product_description` text DEFAULT NULL,
        `product_price` int DEFAULT NULL,
        `product_seller_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`product_seller_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `order_product` (
        `id` int NOT NULL AUTO_INCREMENT,
        `order_id` int DEFAULT NULL,
        `product_id` int DEFAULT NULL,
        `quantity` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
        )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `address` (
        `id` int NOT NULL AUTO_INCREMENT,
        `street` varchar(255) DEFAULT NULL,
        `city` varchar(255) DEFAULT NULL,
        `state` varchar(255) DEFAULT NULL,
        `zip` varchar(255) DEFAULT NULL,
        `user_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `post` (
        `id` int NOT NULL AUTO_INCREMENT,
        `post_title` varchar(255) DEFAULT NULL,
        `post_time` datetime DEFAULT NULL,
        `post_text` text DEFAULT NULL,
        `user_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `event` (
        `id` int NOT NULL AUTO_INCREMENT,
        `event_title` varchar(255) DEFAULT NULL,
        `event_organizer` varchar(255) DEFAULT NULL,
        `event_description` text DEFAULT NULL,
        `event_start` datetime DEFAULT NULL,
        `event_end` datetime DEFAULT NULL,
        PRIMARY KEY (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `note` (
        `id` int NOT NULL AUTO_INCREMENT,
        `note_title` varchar(255) DEFAULT NULL,
        `note_text` text DEFAULT NULL,
        `note_creation_time` datetime DEFAULT NULL,
        `note_update_time` datetime DEFAULT NULL,
        `note_taker_id` int NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`note_taker_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `order` (
        `id` int NOT NULL AUTO_INCREMENT,
        `order_id` int DEFAULT NULL,
        `order_status` int DEFAULT NULL,
        `user_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `category` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `name` (`name`)
        )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `product_category` (
        `id` int NOT NULL AUTO_INCREMENT,
        `product_id` int DEFAULT NULL ,
        `category_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
        FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
      )""")
