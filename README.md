# 1С:Предприятие. Облачная подсистема Фреш в Docker
Позволяет в течении ~30 минут развернуть рабочий стенд подсистемы Фреш с использованием технологии docker.
Может пригодится для:
- Разработки конфигурации которая должно работать в облаке
- Разработки самой технологии Фреш
- Тестирования средств адаптации конфигураций
- и т.д.

## Системные требования
- Оперативной памяти от 4Гб
	- Лучше от 8Гб
- Свободного места от 50Гб
- ПО:
-- [Python 3+](https://www.python.org/downloads/ "Python 3+")
-- [Docker](https://docs.docker.com/engine/install/ "Docker")
-- [Docker Compose](https://docs.docker.com/compose/install/ "Docker Compose")

## Дистрибутивы необходимые для развертывания
Для развертывания стенда потребуются дистрибутивы платформы 1С Предприятие и подсистемы Фреш
- [Платформа 1С Предприятие 8.3](https://releases.1c.ru/project/Platform83 "Платформа 1С Предприятие 8.3") требуется два файла
	- Клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем
	- Cервер 1С:Предприятия (64-bit) для RPM-based Linux-систем
- [Дистрибутивы компонентов 1cFresh](https://releases.1c.ru/project/FreshPublic "Дистрибутивы компонентов 1cFresh")
	- Сайт 1cFresh
	- Форум 1cFresh
	- Шлюз приложений для DEB-based Linux-систем
	- Конфигурация **Менеджер сервиса**
	- Конфигурация **Агент сервиса**
	- Конфигурация **Менеджер доступности**
- [1С:Библиотека технологии сервиса, редакция 1.2](https://releases.1c.ru/version_files?nick=SMTL12&ver=1.2.2.26 "1С:Библиотека технологии сервиса, редакция 1.2") или [1С:Библиотека технологии сервиса, редакция 2.0](https://releases.1c.ru/project/SMTL20 "1С:Библиотека технологии сервиса, редакция 2.0")

<details>
  <summary>Компоненты используемые для тестирования</summary>
- [1С Предприятие 8.3.15.1869](https://releases.1c.ru/version_files?nick=Platform83&ver=8.3.15.1869 "1С Предприятие 8.3.15.1869")
	- [Клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем](https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.15.1869&path=Platform\8_3_15_1869\client_8_3_15_1869.rpm64.tar.gz "Клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем")
	- [Cервер 1С:Предприятия (64-bit) для RPM-based Linux-систем](https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.15.1869&path=Platform\8_3_15_1869\rpm64_8_3_15_1869.tar.gz "Cервер 1С:Предприятия (64-bit) для RPM-based Linux-систем")
- [1С:Предприятие. Облачная подсистема Фреш 1.0.28.1](https://releases.1c.ru/version_files?nick=FreshPublic&ver=1.0.28.1 "1С:Предприятие. Облачная подсистема Фреш 1.0.28.1")
	- [Сайт 1cFresh 1.2.14.1](https://releases.1c.ru/version_file?nick=FreshPublic&ver=1.0.28.1&path=FreshPublic\1_0_28_1\Extrafiles\site_1.2.14.zip "Сайт 1cFresh 1.2.14.1")
	- [Форум 1cFresh 1.0.41.1](https://releases.1c.ru/version_file?nick=FreshPublic&ver=1.0.28.1&path=FreshPublic\1_0_28_1\Extrafiles\forum_1.0.41.zip "Форум 1cFresh 1.0.41.1")
	- [Шлюз приложений 1.1.1.8 для DEB-based Linux-систем ](https://releases.1c.ru/version_file?nick=FreshPublic&ver=1.0.28.1&path=FreshPublic\1_0_28_1\Extrafiles\appgate_1.1.1.8_1_all.deb "Шлюз приложений 1.1.1.8 для DEB-based Linux-систем ")
	- [Менеджер сервиса. Версия 1.0.94.20](https://releases.1c.ru/version_file?nick=FreshPublic&ver=1.0.28.1&path=SM\1_0_94_20\SM_1_0_94_20_setup1c.exe "Менеджер сервиса. Версия 1.0.94.20")
	- [Агент сервиса. Версия 1.0.29.4](https://releases.1c.ru/version_file?nick=FreshPublic&ver=1.0.28.1&path=SA\1_0_29_4\SA_1_0_29_4_setup1c.exe "Агент сервиса. Версия 1.0.29.4")
	- [Менеджер доступности. Версия 1.0.3.4](https://releases.1c.ru/version_file?nick=FreshPublic&ver=1.0.28.1&path=AM\1_0_3_4\AM_1_0_3_4_setup1c.exe "Менеджер доступности. Версия 1.0.3.4")
- [1С:Библиотека технологии сервиса, редакция 1.2. Версия 1.2.2.26](https://releases.1c.ru/version_files?nick=SMTL12&ver=1.2.2.26 "1С:Библиотека технологии сервиса, редакция 1.2. Версия 1.2.2.26")
</details>
## Подготовка к развертыванию
##### Клонирование репозитория
```bash
git clone https://github.com/WizaXxX/docker_fresh.git
cd docker_fresh
```

##### Размещение дистрибутитов
Все ранее  скачанные дистрибутивы необходимо разместить в каталоге `/docker_fresh/distr/`.
После добавления всех дистрибутивов в каталог, он должен выглядить примерно следующим образом
![](https://i.ibb.co/S50sF96/2020-04-10-16-03-22.png)  

##### Настройка списка создваемых информационных баз
В файле `/docker_fresh/other_files/params.json` расположен список информационных баз в формате **JSON** которые требуется создать
- Информационная база **SM** всегда должна быть первой в списке
- Для каждой базы необходимо прописать имя **CF** файла расположенного в каталоге`/docker_fresh/distr/`
- В данный список можно добавить свои информационные базы