Flappy Bird:
1. Управление птичкой, и начало игры управляется пробелом
2. Для того чтобы поменять: 
    цвет труб - клавиша g(green), p(red);
    цвет птички - r(red), b(blue), y(yellow);
    фон - n(night), d(day);
3. В cli требуется ввести имя, для сохранения результата в json файле
4. Реализовано все по требованиям игры
Из бонусов:
    сохранение результатов игрока, шейринг своего рекордного результата

UPDATE: 
1. подключение к базе данных на локальном хосту(осуществленно через PostgreSQL)
2. вывод пойнтов топ 5 игроков через клавишу t(дабл-клик - можно убрать результаты с экрана)
3. вывод лучшего результата и результата юзера через дб на главном меню
4. количество пойнтов у игрока в дб обновляется только если он побил свой предыдущий рекорд