# Fitness Tracker

### Описание:
Программный модуль фитнес-трекера обрабатывает данные для трёх видов тренировок: бега, спортивной ходьбы и плавания. 

Модуль выполняет следующие функции:  
* принимает от блока датчиков информацию о прошедшей тренировке
* определяет вид тренировки
* рассчитывает результаты тренировки
* выводит информационное сообщение о результатах тренировки

Информационное сообщение включает следующие данные:
* тип тренировки (бег, ходьба или плавание)
* длительность тренировки
* дистанция, которую преодолел пользователь, в километрах
* средняя скорость на дистанции, в км/ч
* расход энергии, в килокалориях

Работа датчиков сымитирована в функции main()- пакеты данных передаются в виде кортежа, первый элемент которого — кодовое обозначение прошедшей тренировки, второй — список показателей, полученных от датчиков устройства.
