CREATE DATABASE account_book;
USE account_book;

CREATE TABLE `users_user` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) NULL,
    `is_superuser` bool NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `date_joined` datetime(6) NOT NULL,
    `email` varchar(255) NOT NULL UNIQUE
);

CREATE TABLE `users_user_groups` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` bigint NOT NULL,
    `group_id`
    integer NOT NULL
);

CREATE TABLE `users_user_user_permissions` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` bigint NOT NULL,
    `permission_id` integer NOT NULL
);

ALTER TABLE `users_user_groups` ADD CONSTRAINT `users_user_groups_user_id_group_id_b88eab82_uniq` UNIQUE (`user_id`, `group_id`);
ALTER TABLE `users_user_groups` ADD CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`);
ALTER TABLE `users_user_groups` ADD CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `users_user_user_permissions` ADD CONSTRAINT `users_user_user_permissions_user_id_permission_id_43338c45_uniq` UNIQUE (`user_id`, `permission_id`);
ALTER TABLE `users_user_user_permissions` ADD CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`);
ALTER TABLE `users_user_user_permissions` ADD CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);


CREATE TABLE `article_articlemodels` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `use_money` integer NOT NULL,
    `content` longtext NULL,
    `spending_date` date NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6)NOT NULL,
    `writer_id` bigint NOT NULL
    );

CREATE TABLE `article_shortcuturlmodels` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `link` varchar(255) NOT NULL,
    `new_link` varchar(200) NOT NULL,
    `is_using` bool NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `linked_article_id` bigint NOT NULL,
    `make_user_id` bigint NOT NULL
);

ALTER TABLE `article_articlemodels` ADD CONSTRAINT `article_articlemodels_writer_id_65115b5a_fk_users_user_id` FOREIGN KEY (`writer_id`) REFERENCES `users_user` (`id`);
ALTER TABLE `article_shortcuturlmodels` ADD CONSTRAINT `article_shortcuturlm_linked_article_id_7e74a847_fk_article_a` FOREIGN KEY (`linked_article_id`) REFERENCES `article_articlemodels` (`id`);
ALTER TABLE `article_shortcuturlmodels` ADD CONSTRAINT `article_shortcuturlmodels_make_user_id_c3264c7c_fk_users_user_id` FOREIGN KEY (`make_user_id`) REFERENCES `users_user` (`id`);

