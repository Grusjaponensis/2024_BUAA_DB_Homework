USE CatsTrack;

-- 创建一些初始数据
-- admin email: admin@admin.com
-- admin user_id: da9f23692f66491c921142fbf72a74a5
-- admin hashed_password: $2b$12$WyQOtsmI/3eYusNDTUXHJ.QGM3Ok8hWOT2jaj.Uvkm1aQxGKX4kKe

INSERT INTO cat VALUE (
   '小猫1',
   false,
   2,
   1,
   NULL,
   CURRENT_TIMESTAMP,
   'dad45ca4fda74e1eb925d35156800530'
);

INSERT INTO post VALUE (
    '1491aae2274043e6b799716ae792c8ca',
    'da9f23692f66491c921142fbf72a74a5',
    'dad45ca4fda74e1eb925d35156800530',
    '测试帖',
    '这里是第一篇测试帖。',
    CURRENT_TIMESTAMP
);

INSERT INTO posttag VALUE (
    'a0b773e50f2c47d29f821fe709594308',
    'da9f23692f66491c921142fbf72a74a5',
    '测试标签'
);

INSERT INTO posttagrelation VALUE (
    '1491aae2274043e6b799716ae792c8ca',
    'a0b773e50f2c47d29f821fe709594308'
);