&НаСервере
Процедура Команда1НаСервере()
    Соединение = Новый HTTPСоединение(
        "10.42.0.127", // сервер (хост)
        8000, // порт, по умолчанию для http используется 80, для https 443
        , // пользователь для доступа к серверу (если он есть)
        , // пароль для доступа к серверу (если он есть)
        , // здесь указывается прокси, если он есть
        , // таймаут в секундах, 0 или пусто - не устанавливать
          // защищенное соединение, если используется https
    );
    Заголовки = Новый Соответствие;
    Заголовки.Вставить("X-API-KEY", "123");
	Заголовки.Вставить("X-COMPANY-SYS", "Ogonek");
	Заголовки.Вставить("X-COMPANY-KEY", "Ogonek1");
	Заголовки.Вставить("Content-Type", "application/json;");
	URLЗапрос = Новый HTTPЗапрос("/sync/company/?format=json", Заголовки);
    // Запись JSON

    Данные = Новый Структура;
    Данные.Вставить("short_name", "ООО Огонек");
	Данные.Вставить("full_name", "Общество с ограниченной ответственностью Огонек");
    Данные.Вставить("inn", "151267139");
    Данные.Вставить("kpp", "5123573234");
	
    ЗаписьJSON = Новый ЗаписьJSON;
    тПараметрыJSON = Новый ПараметрыЗаписиJSON(ПереносСтрокJSON.Нет, " ", Истина);  
    ЗаписьJSON.УстановитьСтроку(тПараметрыJSON); 
	ЗаписатьJSON(ЗаписьJSON, Данные);
	//СериализаторXDTO.ЗаписатьJSON(ЗаписьJSON, Данные);
    СтрокаJS = ЗаписьJSON.Закрыть();
    Сообщить("JSON: " + СтрокаJS);
    // Конец JSON
	URLЗапрос.УстановитьТелоИзСтроки(СтрокаJS);
    Результат = Соединение.ОтправитьДляОбработки(URLЗапрос);
    Сообщить("Нам вернули код: " + Результат.КодСостояния);     
	Сообщить("Тело результата: " + Результат.ПолучитьТелоКакСтроку());
КонецПроцедуры

&НаКлиенте
Процедура Команда1(Команда)
	Команда1НаСервере();
КонецПроцедуры

&НаСервере
Процедура Команда2НаСервере()
    Соединение = Новый HTTPСоединение(
        "10.42.0.127", // сервер (хост)
        8000, // порт, по умолчанию для http используется 80, для https 443
        , // пользователь для доступа к серверу (если он есть)
        , // пароль для доступа к серверу (если он есть)
        , // здесь указывается прокси, если он есть
        , // таймаут в секундах, 0 или пусто - не устанавливать
          // защищенное соединение, если используется https
    );
    Заголовки = Новый Соответствие;
    Заголовки.Вставить("X-API-KEY", "123");
	Заголовки.Вставить("X-COMPANY-SYS", "Ogonek");
	Заголовки.Вставить("X-COMPANY-KEY", "Ogonek1");
	Заголовки.Вставить("Content-Type", "application/json;");
	URLЗапрос = Новый HTTPЗапрос("/sync/collection/?format=json", Заголовки);
    // Запись JSON

    Данные = Новый Структура;
    Данные.Вставить("url_name", "rabota");
	Данные.Вставить("public_name", "АктВыполненыхРабот");
    Данные.Вставить("link_name", "ВыполненнаяРабота");
	
    ЗаписьJSON = Новый ЗаписьJSON;
    тПараметрыJSON = Новый ПараметрыЗаписиJSON(ПереносСтрокJSON.Нет, " ", Истина);  
    ЗаписьJSON.УстановитьСтроку(тПараметрыJSON); 
	ЗаписатьJSON(ЗаписьJSON, Данные);
	//СериализаторXDTO.ЗаписатьJSON(ЗаписьJSON, Данные);
    СтрокаJS = ЗаписьJSON.Закрыть();
    Сообщить("JSON: " + СтрокаJS);
    // Конец JSON
	URLЗапрос.УстановитьТелоИзСтроки(СтрокаJS);
    Результат = Соединение.ОтправитьДляОбработки(URLЗапрос);
    Сообщить("Нам вернули код: " + Результат.КодСостояния);     
	Сообщить("Тело результата: " + Результат.ПолучитьТелоКакСтроку());
КонецПроцедуры

&НаКлиенте
Процедура Команда2(Команда)
	Команда2НаСервере();
КонецПроцедуры

&НаСервере
Процедура Команда3НаСервере()
    Соединение = Новый HTTPСоединение(
        "10.42.0.127", // сервер (хост)
        8000, // порт, по умолчанию для http используется 80, для https 443
        , // пользователь для доступа к серверу (если он есть)
        , // пароль для доступа к серверу (если он есть)
        , // здесь указывается прокси, если он есть
        , // таймаут в секундах, 0 или пусто - не устанавливать
          // защищенное соединение, если используется https
    );
    Заголовки = Новый Соответствие;
    Заголовки.Вставить("X-API-KEY", "123");
	Заголовки.Вставить("X-COMPANY-SYS", "Ogonek");
	Заголовки.Вставить("X-COMPANY-KEY", "Ogonek1");
	Заголовки.Вставить("Content-Type", "application/json;");
	URLЗапрос = Новый HTTPЗапрос("/sync/role/?format=json", Заголовки);
    // Запись JSON

    Коллекции = Новый Массив;
	Коллекции.Добавить("rabota");

	Пользователи = Новый Массив;
	Пользователи.Добавить("Alex_1_799"); // Задать имя пользователя

    Данные = Новый Структура;
    Данные.Вставить("name", "Менеджеры");
	Данные.Вставить("collections_list", Коллекции);
    Данные.Вставить("username_list", Пользователи);

    ЗаписьJSON = Новый ЗаписьJSON;
    тПараметрыJSON = Новый ПараметрыЗаписиJSON(ПереносСтрокJSON.Нет, " ", Истина);  
    ЗаписьJSON.УстановитьСтроку(тПараметрыJSON); 
	ЗаписатьJSON(ЗаписьJSON, Данные);
	//СериализаторXDTO.ЗаписатьJSON(ЗаписьJSON, Данные);
    СтрокаJS = ЗаписьJSON.Закрыть();
    Сообщить("JSON: " + СтрокаJS);
    // Конец JSON
	URLЗапрос.УстановитьТелоИзСтроки(СтрокаJS);
    Результат = Соединение.ОтправитьДляОбработки(URLЗапрос);
    Сообщить("Нам вернули код: " + Результат.КодСостояния);     
	Сообщить("Тело результата: " + Результат.ПолучитьТелоКакСтроку());
КонецПроцедуры

&НаКлиенте
Процедура Команда3(Команда)
	Команда3НаСервере();
КонецПроцедуры

&НаСервере
Процедура Команда4НаСервере()
    // Пользователь
    Соединение = Новый HTTPСоединение(
        "10.42.0.127", // сервер (хост)
        8000, // порт, по умолчанию для http используется 80, для https 443
        , // пользователь для доступа к серверу (если он есть)
        , // пароль для доступа к серверу (если он есть)
        , // здесь указывается прокси, если он есть
        , // таймаут в секундах, 0 или пусто - не устанавливать
          // защищенное соединение, если используется https
    );
    Заголовки = Новый Соответствие;
    Заголовки.Вставить("X-API-KEY", "123");
	Заголовки.Вставить("X-COMPANY-SYS", "Ogonek");
	Заголовки.Вставить("X-COMPANY-KEY", "Ogonek1");
	Заголовки.Вставить("Content-Type", "application/json;");
	URLЗапрос = Новый HTTPЗапрос("/sync/user/?format=json", Заголовки);
    // Запись JSON

    Данные = Новый Структура;
    Данные.Вставить("username", "Alex");
	Данные.Вставить("first_name", "Алексей");
	
    ЗаписьJSON = Новый ЗаписьJSON;
    тПараметрыJSON = Новый ПараметрыЗаписиJSON(ПереносСтрокJSON.Нет, " ", Истина);  
    ЗаписьJSON.УстановитьСтроку(тПараметрыJSON); 
	ЗаписатьJSON(ЗаписьJSON, Данные);
	//СериализаторXDTO.ЗаписатьJSON(ЗаписьJSON, Данные);
    СтрокаJS = ЗаписьJSON.Закрыть();
    Сообщить("JSON: " + СтрокаJS);
    // Конец JSON
	URLЗапрос.УстановитьТелоИзСтроки(СтрокаJS);
    Результат = Соединение.ОтправитьДляОбработки(URLЗапрос);
    Сообщить("Нам вернули код: " + Результат.КодСостояния);     
	Сообщить("Тело результата: " + Результат.ПолучитьТелоКакСтроку());
КонецПроцедуры

&НаКлиенте
Процедура Команда4(Команда)
	Команда4НаСервере();
КонецПроцедуры


&НаСервере
Процедура Команда5НаСервере()
    Соединение = Новый HTTPСоединение(
        "10.42.0.127", // сервер (хост)
        8000, // порт, по умолчанию для http используется 80, для https 443
        , // пользователь для доступа к серверу (если он есть)
        , // пароль для доступа к серверу (если он есть)
        , // здесь указывается прокси, если он есть
        , // таймаут в секундах, 0 или пусто - не устанавливать
          // защищенное соединение, если используется https
    );
    Заголовки = Новый Соответствие;
    Заголовки.Вставить("X-API-KEY", "123");
	Заголовки.Вставить("X-COMPANY-SYS", "Ogonek");
	Заголовки.Вставить("X-COMPANY-KEY", "Ogonek1");
	Заголовки.Вставить("Content-Type", "application/json;");
	URLЗапрос = Новый HTTPЗапрос("/sync/docs/?format=json", Заголовки);
    // Запись JSON
	Запрос = Новый Запрос(
        "ВЫБРАТЬ
        |  *
        |ИЗ
        |  Документ.АктВыполненыхРабот"
    );
    РезультатЗапроса = Запрос.Выполнить();
	ВыборкаДокументов = РезультатЗапроса.Выбрать();
	Список = Новый Массив;
	Пока ВыборкаДокументов.Следующий() Цикл
		Док1С = Новый Структура;
		ДокСырой = ВыборкаДокументов.Ссылка.ПолучитьОбъект();
		Док1С.Вставить("Ref", Строка(ДокСырой.Ссылка.УникальныйИдентификатор()));
		Док1С.Вставить("Date", Строка(ДокСырой.Дата));
		Док1С.Вставить("Number", Строка(ДокСырой.Номер)); 		
		Док1С.Вставить("Posted", ДокСырой.Проведен);
		Док1С.Вставить("DeletionMark", ДокСырой.ПометкаУдаления);

        Док1С.Вставить("Название", Строка(ДокСырой));
        Док1С.Вставить("Клиент", Строка(ДокСырой.Клиент));
        Док1С.Вставить("Услуги", Строка(ДокСырой.Услуги));
		Список.Добавить(Док1С);
		//Список.Добавить(ВыборкаДокументов.Ссылка.ПолучитьОбъект());
    КонецЦикла;

    Роли = Новый Массив;
	Роли.Добавить("Менеджеры");
	
	Данные = Новый Структура;
	Данные.Вставить("url_name", "rabota");
    Данные.Вставить("role_list", Роли);
	Данные.Вставить("docs", Список);

    ЗаписьJSON = Новый ЗаписьJSON;
    тПараметрыJSON = Новый ПараметрыЗаписиJSON(ПереносСтрокJSON.Нет, " ", Истина);  
    ЗаписьJSON.УстановитьСтроку(тПараметрыJSON); 
	ЗаписатьJSON(ЗаписьJSON, Данные);
	//СериализаторXDTO.ЗаписатьJSON(ЗаписьJSON, Данные);
    СтрокаJS = ЗаписьJSON.Закрыть();
    Сообщить("JSON: " + СтрокаJS);
    // Конец JSON
	URLЗапрос.УстановитьТелоИзСтроки(СтрокаJS);
    Результат = Соединение.ОтправитьДляОбработки(URLЗапрос);
    Сообщить("Нам вернули код: " + Результат.КодСостояния);     
	Сообщить("Тело результата: " + Результат.ПолучитьТелоКакСтроку());
КонецПроцедуры

&НаКлиенте
Процедура Команда5(Команда)
	Команда5НаСервере();
КонецПроцедуры
