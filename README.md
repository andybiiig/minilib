# Краткое руководство по использованию программы minilib

Программа minilib подготовлена в качестве решения тестового задания с целью показать навыки программирования на языке
Python.

## Общие принципы

Программа minilib является консольным приложением. Для навигации и управления в ней ***не используются*** клавиши
управления курсором и манипулятор мышь. Навигация по меню осуществляется путем ввода номера соответствующего пункта
меню и подтверждения ввода нажатием клавиши Enter.

Ввод пустой строки вместо требуемого значения при добавлении или поиске книги, а также вместо номера пункта меню 
во всех меню, кроме главного, приведет к _отмене_ текущей операции. Ввод пустой строки в главном меню считается ошибкой
ввода пользователя и не будет иметь последствий кроме сообщения `Неверный ввод`.

Обо всех выполненных операциях программа информирует пользователя специальным сообщением, например:

    [ИНФОРМАЦИЯ] Данные загружены

При возникновении ошибок программа также сообщает о них, например:

    [ОШИБКА] Книга с таким id не найдена
       Нажмите Enter для продолжения

Ошибки требуют дополнительного внимания пользователя, поэтому они ожидают подтверждения (нажатия клавиши Enter).

Некоторые ошибки являются фатальными и при их возникновении дальнейшая работа программы невозможна. О таких ошибках
программа также предупредит, после чего завершит свою работу, например:

    [ФАТАЛЬНАЯ ОШИБКА] Ошибка при разборе содержимого файла <имя файла-хранилища>
       Нажмите Enter для продолжения

## Запуск программы

При запуске программа выполняет загрузку книг из файла-хранилища .json, имя которого указано в переменной
`LIBRARY_FILENAME`. При удачной загрузке будет выведено сообщение, после чего программа перейдет в режим главного меню.

    [ИНФОРМАЦИЯ] Данные загружены

Отсутствие файла-хранилища на этом этапе не является ошибкой - такой запуск считается первичным. Программа выведет
соответствующее сообщение, после чего перейдет в режим главного меню.

    [ИНФОРМАЦИЯ] Файл <имя файла-хранилища> не найден, запуск считается первичным

** Функционал передачи имени файла-хранилища через командную строку или файл конфигурации не реализован, так как это не
требовалось по условиям тестового задания. 

## Главное меню

На экран будет выведено главное меню программы.

     -> Главное меню библиотеки <-
      1. Добавление книги
      2. Удаление книги
      3. Поиск книг...
      4. Отображение всех книг
      5. Изменение статуса книги
      0. Выход
    Выберите действие: 

Пользователю необходимо выбрать требуемое действие путем ввода номера пункта меню и подтвердить свой выбор, нажав Enter

## Добавление книги

При выборе соответствующего пункта меню на экран ***последовательно*** будут выведены запросы для ввода данных книги.

    Введите название книги (пустая строка для отмены): _
    Введите автора книги (пустая строка для отмены): _
    Введите год издания книги не ранее 1457 (пустая строка для отмены): _

Для добавления книги в библиотеку должны быть заполнены все данные. При вводе пустой строки на любом этапе будет
выведено соответствующее сообщение и книга добавлена не будет.

    [ИНФОРМАЦИЯ] Добавление книги отменено

При успешном заполнении всех данных книга будет добавлена в библиотеку, а на экран будет выведено сообщение.

    [ИНФОРМАЦИЯ] Книга добавлена

## Удаление книги

При выборе соответствующего пункта меню на экран будет выведена подсказка.

    Введите id книги для удаления (пустая строка для отмены):

При вводе пустой строки будет выведено соответствующее сообщение и книга удалена не будет.

    [ИНФОРМАЦИЯ] Удаление книги отменено

При вводе корректного числового значения будет выполнена попытка удаления книги с указанным ID. В случае отсутствия 
такой книги на экран будет выведено сообщение об ошибке.

    [ОШИБКА] Книга с таким id не найдена
       Нажмите Enter для продолжения

Если книга с указанным ID в библиотеке была, она будет удалена, а на экран будет выведено сообщение.

    [ИНФОРМАЦИЯ] Книга удалена

## Поиск книг

Поскольку точный ввод текстового значения может представлять трудность для пользователя, поиск книг по названию
и по автору осуществляется по наличию введенной подстроки в указанном поле.
Например, при вводе подстроки "старик" будут найдены книги "Старик и море", "Старик Хоттабыч" и "Дневник безумного
старика". Поиск является ***регистронезависимым***, то есть строчные и прописные буквы не различаются. 

После выбора в главном меню соответствующего пункта на экран будет выведено меню поиска.

    Поиск книг:
      1. По названию
      2. По автору
      3. По году издания
      4. По статусу
    Выберите действие (пустая строка для отмены): 

После ввода номера пункта и нажатия Enter программа перейдет в режим поиска по выбранному критерию. Нажатие Enter без
указания номера пункта отменяет поиск и возвращает в главное меню.

### Поиск книг по названию

При выборе данного пункта программа предложит ввести подстроку для поиска книг по названию.

    Введите подстроку для поиска по названию книги (пустая строка для отмены):

После ввода подстроки поиска и нажатия на Enter программа выведет перечень найденных книг. 
   
     Найдено 3 книг
    +----+------------------+-----------------+-----------+---------+
    | id |     Название     |      Автор      |Год издания|  Статус |
    +----+------------------+-----------------+-----------+---------+
    |  1 |Мастер и Маргарита|Михаил Булгаков  |    1940   |в наличии|
    |  5 |Граф Монте-Кристо |Александр Дюма   |    1963   |в наличии|
    |  6 |Три товарища      |Эрих Мария Ремарк|    1950   |выдана   |
    +----+------------------+-----------------+-----------+---------+
       Нажмите Enter для продолжения

В случае, если критерию поиска не соответствует ни одна книга, программа сообщит об этом.

    [ИНФОРМАЦИЯ] Книг c подходящим названием не найдено
       Нажмите Enter для продолжения

После нажатия на Enter программа вернется в меню поиска.

При вводе пустой подстроки текущий поиск будет отменен, о чем программа сообщит и вернется в меню поиска.

    [ИНФОРМАЦИЯ] Поиск отменен

### Поиск книг по автору

Поиск книг по автору полностью аналогичен поиску по названию. 

### Поиск книг по году издания

Поиск книг по году издания аналогичен поиску по названию с той лишь разницей, что год должен быть указан точно,
поиск по подстроке не осуществляется. Ввод нечислового значения считается неверным, о чем программа сообщит и предложит
повторить ввод.

    Введите год издания книги (пустая строка для отмены): ыыы
    Неверный ввод
    Введите год издания книги (пустая строка для отмены): 


### Поиск книг по статусу

При выборе данного пункта программа предложит указать один из статусов, поддерживаемых библиотекой в данной версии
(может быть расширен позднее).

     Укажите статус книги:
      1. в наличии
      2. выдана
    Введите номер статуса (пустая строка для отмены): 

После ввода номера статуса и нажатия на Enter программа выведет перечень найденных книг. 

     Найдено 1 книг
    +----+------------+-----------------+-----------+------+
    | id |  Название  |      Автор      |Год издания|Статус|
    +----+------------+-----------------+-----------+------+
    |  6 |Три товарища|Эрих Мария Ремарк|    1950   |выдана|
    +----+------------+-----------------+-----------+------+
       Нажмите Enter для продолжения

Если книги с указанным статусом в библиотеке отсутствуют, об этом будет выведено сообщение.

    [ИНФОРМАЦИЯ] Книг c указанным статусом не найдено
       Нажмите Enter для продолжения

При вводе пустой подстроки вместо номера статуса текущий поиск будет отменен, о чем программа сообщит и вернется в меню
поиска.

    [ИНФОРМАЦИЯ] Поиск отменен


## Отображение всех книг

При выборе данного пункта программа отобразит все книги, учтенные в библиотеке на данный момент. После нажатия на
клавишу Enter будет осуществлен возврат в главное меню. 

     Все книги нашей библиотеки
    +----+------------------+-------------------------+-----------+---------+
    | id |     Название     |          Автор          |Год издания|  Статус |
    +----+------------------+-------------------------+-----------+---------+
    |  1 |Мастер и Маргарита|Михаил Булгаков          |    1940   |в наличии|
    |  2 |Собачье сердце    |Михаил Булгаков          |    1925   |в наличии|
    |  3 |Двенадцать стульев|Илья Ильф, Евгений Петров|    1928   |в наличии|
    |  4 |Мертвые души      |Николай Гоголь           |    1842   |в наличии|
    |  5 |Граф Монте-Кристо |Александр Дюма           |    1963   |в наличии|
    |  6 |Три товарища      |Эрих Мария Ремарк        |    1950   |выдана   |
    |  7 |Отверженные       |Виктор Гюго              |    1950   |в наличии|
    +----+------------------+-------------------------+-----------+---------+
       Нажмите Enter для продолжения

## Изменение статуса книги

При выборе данного пункта меню программа предложит ввести id книги, статус которой необходимо изменить. Нечисловой ввод
считается неверным, о чем программа сообщит и предложит ввести id еще раз.

    Введите id книги для изменения статуса (пустая строка для отмены): й
    Неверный ввод
    Введите id книги для изменения статуса (пустая строка для отмены): 

После ввода id программа сразу проверяет наличие такой книги в библиотеке. При отсутствии книги будет выведено
сообщение об ошибке, а программа вернется в главное меню.

    [ОШИБКА] Книга с таким id не найдена
       Нажмите Enter для продолжения

В случае, когда книга с указанным id имеется в библиотеке, программа предложит выбрать для нее статус по номеру. 

     Доступные статусы:
      1. в наличии
      2. выдана
    Введите номер статуса (пустая строка для отмены): 

После выбора номера статуса и нажатия Enter статус книги с указанным id будет изменен и программа вернется в главное
меню.

    [ИНФОРМАЦИЯ] Статус книги изменен

В случаях, когда вместо id книги или номер статуса введена пустая строка, изменение статуса будет отменено, о чем
программа сообщит и вернется в главное меню. 

    [ИНФОРМАЦИЯ] Изменение статуса книги отменено


## Завершение работы программы

В ходе работы программа фиксирует, вносились ли изменения в библиотеку (добавление и удаление книг, изменение статуса).
В случае, если изменения вносились, программа попытается сохранить содержимое библиотеки в файл. Об успешности этой
операции свидетельствует сообщение:

    [ИНФОРМАЦИЯ] Данные сохранены

В случае, если изменения не вносились, программа также сообщит об этом: 

    [ИНФОРМАЦИЯ] Данные не изменены, сохранение не требуется

На этом работа с программой будет завершена.