from sqlalchemy.orm import Session
from typing import Dict, List, Tuple
from app.models.assessment import AssessmentResult

CATEGORIES = [
    "IT_ENGINEERING", "DATA_AI", "MEDICINE", "BUSINESS",
    "LAW", "DESIGN_CREATIVE", "SOCIAL_SCIENCES", "EDUCATION",
]

MAJORS_MAP = {
    "IT_ENGINEERING":  ["Software Engineering", "Cybersecurity", "Computer Science", "Information Systems"],
    "DATA_AI":         ["Artificial Intelligence", "Data Science", "Machine Learning", "Applied Mathematics"],
    "MEDICINE":        ["General Medicine", "Nursing", "Biomedical Science", "Public Health"],
    "BUSINESS":        ["Business Administration", "Finance", "Marketing", "International Business"],
    "LAW":             ["International Law", "Corporate Law", "Public Policy", "Political Science"],
    "DESIGN_CREATIVE": ["Graphic Design", "Digital Media", "Architecture", "Animation"],
    "SOCIAL_SCIENCES": ["Psychology", "Sociology", "International Relations", "Communications"],
    "EDUCATION":       ["Education Studies", "TESOL", "Pedagogy", "Educational Technology"],
}

# Weights are language-independent — defined once, reused across all languages
_W = [
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"DESIGN_CREATIVE": 3, "SOCIAL_SCIENCES": 1}, {"MEDICINE": 3, "EDUCATION": 1}, {"BUSINESS": 3, "LAW": 1}],
    [{"EDUCATION": 3, "SOCIAL_SCIENCES": 1}, {"IT_ENGINEERING": 2, "DATA_AI": 2}, {"EDUCATION": 2, "SOCIAL_SCIENCES": 2}, {"MEDICINE": 2, "EDUCATION": 2}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"SOCIAL_SCIENCES": 3, "LAW": 1}, {"DESIGN_CREATIVE": 3, "BUSINESS": 1}, {"MEDICINE": 3, "DATA_AI": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 2}, {"LAW": 3, "BUSINESS": 1}, {"MEDICINE": 3, "SOCIAL_SCIENCES": 1}, {"DESIGN_CREATIVE": 3, "SOCIAL_SCIENCES": 1}],
    [{"IT_ENGINEERING": 2, "BUSINESS": 2}, {"SOCIAL_SCIENCES": 2, "LAW": 2}, {"DATA_AI": 2, "MEDICINE": 2}, {"DESIGN_CREATIVE": 2, "EDUCATION": 2}],
    [{"IT_ENGINEERING": 2, "DATA_AI": 2}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"MEDICINE": 3, "EDUCATION": 1}, {"BUSINESS": 3, "IT_ENGINEERING": 1}],
    [{"DATA_AI": 3, "IT_ENGINEERING": 1}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"SOCIAL_SCIENCES": 3, "MEDICINE": 1}, {"DESIGN_CREATIVE": 2, "EDUCATION": 2}],
    [{"IT_ENGINEERING": 2, "DATA_AI": 2}, {"LAW": 2, "BUSINESS": 2}, {"MEDICINE": 3, "SOCIAL_SCIENCES": 1}, {"DESIGN_CREATIVE": 3, "EDUCATION": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"SOCIAL_SCIENCES": 3, "MEDICINE": 1}, {"DESIGN_CREATIVE": 3, "EDUCATION": 1}, {"BUSINESS": 3, "LAW": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"BUSINESS": 3, "DATA_AI": 1}, {"EDUCATION": 3, "SOCIAL_SCIENCES": 1}, {"DESIGN_CREATIVE": 3, "IT_ENGINEERING": 1}],
    [{"DATA_AI": 3, "IT_ENGINEERING": 1}, {"BUSINESS": 2, "LAW": 1}, {"SOCIAL_SCIENCES": 2, "EDUCATION": 2}, {"MEDICINE": 3, "DATA_AI": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"SOCIAL_SCIENCES": 2, "EDUCATION": 2}, {"DESIGN_CREATIVE": 1, "BUSINESS": 1}],
    [{"DATA_AI": 3, "IT_ENGINEERING": 2}, {"MEDICINE": 3, "SOCIAL_SCIENCES": 1}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"DESIGN_CREATIVE": 3, "BUSINESS": 1}],
    [{"EDUCATION": 3, "SOCIAL_SCIENCES": 1}, {"MEDICINE": 3, "LAW": 1}, {"DATA_AI": 2, "BUSINESS": 2}, {"LAW": 3, "SOCIAL_SCIENCES": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"DESIGN_CREATIVE": 3, "IT_ENGINEERING": 1}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"BUSINESS": 3, "DATA_AI": 1}],
    [{"DATA_AI": 2, "IT_ENGINEERING": 2}, {"SOCIAL_SCIENCES": 3, "MEDICINE": 1}, {"BUSINESS": 3, "IT_ENGINEERING": 1}, {"DESIGN_CREATIVE": 3, "EDUCATION": 1}],
    [{"EDUCATION": 2, "IT_ENGINEERING": 2}, {"EDUCATION": 2, "DESIGN_CREATIVE": 2}, {"LAW": 2, "EDUCATION": 2}, {"MEDICINE": 3, "SOCIAL_SCIENCES": 1}],
    [{"SOCIAL_SCIENCES": 2, "BUSINESS": 2}, {"LAW": 2, "BUSINESS": 2}, {"MEDICINE": 2, "IT_ENGINEERING": 2}, {"DESIGN_CREATIVE": 2, "DATA_AI": 2}],
    [{"IT_ENGINEERING": 2, "DATA_AI": 2}, {"MEDICINE": 3, "DATA_AI": 1}, {"LAW": 2, "SOCIAL_SCIENCES": 2}, {"DESIGN_CREATIVE": 3, "EDUCATION": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"MEDICINE": 3, "DATA_AI": 1}, {"BUSINESS": 3, "LAW": 1}],
    [{"BUSINESS": 2, "IT_ENGINEERING": 2}, {"EDUCATION": 3, "SOCIAL_SCIENCES": 1}, {"MEDICINE": 3, "SOCIAL_SCIENCES": 1}, {"DESIGN_CREATIVE": 2, "BUSINESS": 2}],
    [{"IT_ENGINEERING": 2, "DATA_AI": 2}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"DESIGN_CREATIVE": 2, "EDUCATION": 2}, {"MEDICINE": 2, "SOCIAL_SCIENCES": 2}],
    [{"IT_ENGINEERING": 2, "DESIGN_CREATIVE": 2}, {"LAW": 2, "DATA_AI": 2}, {"BUSINESS": 2, "DESIGN_CREATIVE": 2}, {"SOCIAL_SCIENCES": 2, "EDUCATION": 2}],
    [{"IT_ENGINEERING": 2, "BUSINESS": 2}, {"MEDICINE": 2, "DATA_AI": 2}, {"LAW": 2, "SOCIAL_SCIENCES": 2}, {"DESIGN_CREATIVE": 3, "EDUCATION": 1}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"MEDICINE": 2, "SOCIAL_SCIENCES": 2}, {"LAW": 2, "SOCIAL_SCIENCES": 2}, {"BUSINESS": 3, "LAW": 1}],
    [{"BUSINESS": 3, "LAW": 1}, {"MEDICINE": 2, "SOCIAL_SCIENCES": 2}, {"DESIGN_CREATIVE": 2, "EDUCATION": 2}, {"IT_ENGINEERING": 2, "DATA_AI": 2}],
    [{"IT_ENGINEERING": 2, "DATA_AI": 2}, {"MEDICINE": 3, "DATA_AI": 1}, {"LAW": 3, "SOCIAL_SCIENCES": 1}, {"BUSINESS": 3, "IT_ENGINEERING": 1}],
    [{"DATA_AI": 3, "IT_ENGINEERING": 1}, {"SOCIAL_SCIENCES": 3, "MEDICINE": 1}, {"DESIGN_CREATIVE": 3, "IT_ENGINEERING": 1}, {"LAW": 2, "BUSINESS": 2}],
    [{"IT_ENGINEERING": 3, "DATA_AI": 1}, {"DESIGN_CREATIVE": 3, "EDUCATION": 1}, {"LAW": 2, "SOCIAL_SCIENCES": 2}, {"BUSINESS": 3, "IT_ENGINEERING": 1}],
    [{"IT_ENGINEERING": 2, "DATA_AI": 2}, {"SOCIAL_SCIENCES": 2, "EDUCATION": 2}, {"MEDICINE": 2, "LAW": 2}, {"DESIGN_CREATIVE": 2, "BUSINESS": 2}],
]

_QUESTIONS_RU = [
    ("У тебя свободный вечер. Что выберешь?", ["Напишу код или собью что-то из железа", "Порисую или создам что-то креативное", "Почитаю про устройство человеческого тела", "Придумаю новую бизнес-идею"]),
    ("Друг не понимает математику. Ты…", ["Объясню — мне нравится учить других", "Напишу программу, которая решит задачу", "Найду крутое видео на YouTube", "Сяду рядом и терпеливо разберу вместе"]),
    ("Какой школьный проект тебя бы зажёг?", ["Создать приложение или сайт", "Написать доклад о глобальном неравенстве", "Разработать логотип и бренд для стартапа", "Исследовать болезнь и представить результаты"]),
    ("Какая суперсила тебе ближе?", ["Моментально разобраться в любой технологии", "Убеждать любого логикой и словами", "Вылечить любую болезнь одним прикосновением", "Создавать искусство, которое трогает миллионы"]),
    ("Как ты решаешь сложную задачу?", ["Разбиваю на шаги и пишу план", "Общаюсь с людьми и собираю мнения", "Сначала глубоко изучаю тему", "Мозгоштурм и новые идеи"]),
    ("Какое кино смотришь с удовольствием?", ["Фантастика про ИИ и технологии будущего", "Судебные драмы и политические триллеры", "Медицинские сериалы и документалки", "Истории о бизнесе и стартапах"]),
    ("Видишь данные об изменении климата. Твоя первая мысль?", ["Как ИИ может помочь это решить?", "Какие законы заставят правительства действовать?", "Как это влияет на психическое здоровье людей?", "Хочу создать кампанию для повышения осведомлённости"]),
    ("Где тебе комфортнее всего работать?", ["Тихо, с наушниками, в глубокой концентрации", "Переговорные, командная работа и дискуссии", "Больница, лаборатория — помогать людям", "Творческая студия с мозгоштурмом"]),
    ("Чем ты больше всего гордишься в себе?", ["Решаю технические задачи, от которых другие отказываются", "Понимаю людей и умею их выслушать", "Делаю вещи красивыми и значимыми", "Организую, веду за собой и достигаю результата"]),
    ("Что бы ты делал каждый день, если бы мог?", ["Кодить новый проект с нуля", "Изучать рынок и писать питч", "Волонтёрить в школе или сообществе", "Фотографировать, снимать или анимировать"]),
    ("Как ты относишься к числам и статистике?", ["Обожаю — паттерны и данные меня захватывают", "Нормально, когда нужно для финансов", "Предпочитаю работать с людьми, а не с цифрами", "Только если связано со здоровьем и биологией"]),
    ("Ты нашёл уязвимость в крупном приложении. Что сделаешь?", ["Сообщу ответственно — это так интересно!", "Подумаю о правовых и этических аспектах", "Напишу статью о рисках для конфиденциальности", "Честно — просто пройду мимо, это не моё"]),
    ("Какая роль в будущем звучит как ты?", ["Исследователь ИИ в технологической компании", "Хирург или врач-специалист", "Международный адвокат по правам человека", "Арт-директор в дизайн-агентстве"]),
    ("Если бы ты мог изменить одну вещь в мире, что это было бы?", ["Сделать качественное образование доступным для всех", "Решить проблему неравенства в здравоохранении", "Использовать ИИ для борьбы с бедностью и голодом", "Реформировать несправедливые законы"]),
    ("Каким инструментом ты хотел бы овладеть?", ["Python или JavaScript для разработки", "Figma или Adobe для дизайна", "Юридические базы данных и прецеденты", "Excel и финансовое моделирование"]),
    ("Какую книгу ты бы реально прочитал для удовольствия?", ["Биография учёного или изобретателя", "Книга по психологии о поведении людей", "История основателя стартапа", "Графический роман или история искусств"]),
    ("Местная школа просит помощи. Что предложишь?", ["Научу детей программированию или робототехнике", "Проведу мастер-класс по театру или арту", "Расскажу об экологическом праве", "Помогу с медосмотрами или первой помощью"]),
    ("Как ты себя чувствуешь в команде?", ["Обожаю — я тот, кто связывает всех", "Нормально, но лучше с чёткой ролью лидера", "Лучше в небольших командах с общей целью", "Предпочитаю работать один над творческими задачами"]),
    ("Какой предмет в школе нравился больше всего?", ["Математика или информатика", "Биология или химия", "История, литература или обществознание", "Рисование, музыка или дизайн"]),
    ("Твоя мечта — первая работа после университета в…", ["Технологическом стартапе", "Международной юридической фирме или НКО", "Больнице или научно-исследовательском институте", "Международной консалтинговой компании"]),
    ("Если бы у тебя был 1 миллион долларов для инвестиций, ты бы…", ["Вложил в ИИ или технологический стартап", "Открыл школу или образовательную платформу", "Построил клинику в отдалённом регионе", "Открыл креативное агентство или медиакомпанию"]),
    ("Что тебя больше всего раздражает в жизни?", ["Системы, которые работают неэффективно", "Несправедливость вокруг меня", "Люди, которые не думают творчески", "Видеть страдающих людей без поддержки"]),
    ("Как ты предпочитаешь представлять свои идеи?", ["Показываю живой демо рабочего продукта", "Подробный письменный отчёт с доказательствами", "Визуальная презентация с сильным дизайном", "Личная история, которая цепляет эмоционально"]),
    ("Кем из реальных людей ты восхищаешься?", ["Технологическим визионером вроде Маска", "Учёным или нобелевским лауреатом", "Правозащитником или юристом", "Художником или творческой иконой"]),
    ("Тебе предлагают летнюю стажировку где угодно. Ты выберешь:", ["Google или Microsoft — команда разработки", "ВОЗ или Красный Крест", "ООН или Amnesty International", "McKinsey, Goldman Sachs или стартап"]),
    ("Насколько важен для тебя высокий доход в карьере?", ["Очень важен — хочу финансовой свободы", "Важен, но влияние на мир важнее", "Готов получать меньше, если занимаюсь любимым делом", "В IT платят хорошо, и работа мне нравится!"]),
    ("Читая новости, что привлекает твоё внимание?", ["Прорывы в ИИ или угрозы кибербезопасности", "Медицинские открытия и эпидемии", "Судебные решения и политические дебаты", "Слияния компаний и раунды финансирования"]),
    ("Какой навык ты хотел бы освоить за 3 года?", ["Машинное обучение и работа с данными", "Эмпатичное консультирование и психология", "UI/UX дизайн и визуальное повествование", "Международные переговоры и публичные выступления"]),
    ("Учитель просит сделать финальный проект. Ты выбираешь:", ["Создать рабочее веб-приложение или бота", "Нарисовать комикс или снять короткометражку", "Написать политическое предложение по социальной проблеме", "Открыть мини-компанию с бизнес-планом"]),
    ("Чего ты больше всего боишься в будущем?", ["Отстать от быстро меняющегося мира технологий", "Выбрать неверный карьерный путь", "Не сделать достаточно для изменения мира к лучшему", "Застрять в работе без творчества"]),
]

_QUESTIONS_EN = [
    ("You have a free afternoon. What sounds most fun?", ["Build something with code or hardware", "Sketch, draw or design something creative", "Read about how the human body works", "Plan a new business idea"]),
    ("Your friend struggles with math. You…", ["Explain it — I love teaching others", "Write a program that solves it for them", "Find a great YouTube video", "Sit beside them and work through it patiently"]),
    ("Which school project would excite you MOST?", ["Create an app or website", "Write a report on global inequality", "Design a logo and brand for a startup", "Research a disease and present findings"]),
    ("Pick the superpower that fits you best:", ["Instantly understand any machine or system", "Persuade anyone with logic and words", "Heal any illness with a touch", "Create art that moves millions of people"]),
    ("What do you do when you have a big problem to solve?", ["Break it into steps and write a plan", "Talk to people and gather opinions", "Research deeply before deciding anything", "Brainstorm creatively and try new ideas"]),
    ("Which movie genre do you enjoy most?", ["Sci-fi with AI and tech dystopias", "Courtroom dramas and political thrillers", "Medical dramas or documentaries", "Business or startup stories"]),
    ("You see data about climate change. Your first thought is…", ["How can AI help predict or solve this?", "What laws could force governments to act?", "How does it affect people's mental health?", "Can I design a campaign to raise awareness?"]),
    ("What does your ideal work environment look like?", ["Quiet desk, headphones, deep focus work", "Meeting rooms, collaboration and debate", "Hospital, lab or clinic helping people", "Creative studio with art and brainstorming"]),
    ("What makes you most proud about yourself?", ["I solve technical problems others give up on", "I understand people and make them feel heard", "I make things look beautiful and meaningful", "I organize, lead and get things done"]),
    ("What would you do every day if you could?", ["Code a new project from scratch", "Research market trends and write a pitch", "Volunteer at a community or school program", "Photograph, film or animate something"]),
    ("How do you feel about working with numbers and statistics?", ["Love it — patterns and data excite me", "Fine with it when needed for finance", "I prefer working with people over numbers", "Only if it relates to health and biology"]),
    ("You discover a security vulnerability in a big app. You…", ["Report it responsibly — this is fascinating!", "Think about the legal and ethical dimensions", "Write an article about user privacy risks", "Honestly, I'd just move on — not my thing"]),
    ("Which future role sounds MOST like you?", ["AI researcher at a tech company", "Surgeon or specialist doctor", "International human rights lawyer", "Creative director at a design agency"]),
    ("If you could change one thing about the world right now, it would be…", ["Make quality education available for everyone", "Fix global healthcare inequality", "Use AI to solve poverty and hunger", "Reform unjust laws and protect human rights"]),
    ("Which tool would you most enjoy mastering?", ["Python or JavaScript for building apps", "Figma or Adobe for design", "Legal research databases and case studies", "Excel and financial modeling tools"]),
    ("What type of book would you actually read for fun?", ["A biography of a scientist or inventor", "A psychology book about human behavior", "A startup founder's story", "A graphic novel or art history book"]),
    ("A local school asks for your help. You offer to…", ["Teach kids coding or robotics", "Run a drama or art workshop", "Give a talk on environmental law", "Help with health screenings or first aid"]),
    ("How do you feel about working in a team?", ["Love it — I'm the one connecting everyone", "Fine, but I prefer leading with a clear role", "Best in small teams focused on a mission", "I work better solo on creative tasks"]),
    ("What was your favorite subject in school?", ["Math or Computer Science", "Biology or Chemistry", "History, Literature or Social Studies", "Art, Music or Design"]),
    ("Your dream first job out of university would be at…", ["A Silicon Valley tech startup", "An international law firm or NGO", "A hospital or research institute", "A global consulting or investment firm"]),
    ("If you had 1 million dollars to invest, you would…", ["Fund an AI or tech startup", "Build a school or learning platform", "Open a clinic in an underserved community", "Start a creative agency or media company"]),
    ("What frustrates you most in your daily life?", ["Systems that don't work efficiently", "Injustice and unfairness around me", "People who don't think creatively", "Seeing people suffer with no support"]),
    ("How do you prefer to present your ideas?", ["Live demo of a working product", "A detailed written report with evidence", "A visual pitch deck with strong design", "A personal story that connects emotionally"]),
    ("Which real person do you admire most?", ["A tech visionary like Elon Musk", "A scientist or Nobel Prize winner", "A human rights activist or lawyer", "An artist or creative icon"]),
    ("You're given a summer internship anywhere. You pick:", ["Google or Microsoft — engineering team", "World Health Organization or Red Cross", "United Nations or Amnesty International", "McKinsey, Goldman Sachs or a startup"]),
    ("How important is financial reward in your dream career?", ["Very important — I want to be wealthy", "Important, but impact matters more", "I'd work for less if I love what I do", "Tech pays well and I love the work!"]),
    ("When you read the news, what stories catch your eye?", ["New AI breakthroughs or cybersecurity threats", "Medical discoveries and health epidemics", "Court rulings and policy debates", "Business mergers and startup funding rounds"]),
    ("Which skill would you most want to master in 3 years?", ["Machine learning and data modeling", "Empathy-driven counseling and therapy", "UI/UX design and visual storytelling", "International negotiation and public speaking"]),
    ("A teacher asks you to create a final project. You choose:", ["Build a working web app or automation tool", "Create an illustrated storybook or short film", "Write a policy proposal for a social issue", "Start a mini-company with a business plan"]),
    ("What's your biggest fear about the future?", ["Falling behind in a fast-changing tech world", "Choosing the wrong career path", "Not making enough of a difference in the world", "Being stuck in a job without creativity"]),
]

_QUESTIONS_KK = [
    ("Сенің бос кешің бар. Не таңдайсың?", ["Код жазамын немесе бір нәрсе жасаймын", "Бір нәрсе сызамын немесе жасаймын", "Адам ағзасы туралы оқимын", "Жаңа бизнес-идея ойлап табамын"]),
    ("Досың математиканы түсінбейді. Сен…", ["Түсіндіремін — үйретуді жақсы көремін", "Есепті шешетін бағдарлама жазамын", "YouTube-тан жақсы бейне табамын", "Қасына отырып бірге шешемін"]),
    ("Қандай мектеп жобасы саған қызықты болар еді?", ["Қолданба немесе сайт жасау", "Жаһандық теңсіздік туралы баяндама жазу", "Стартапқа логотип және бренд жасау", "Ауру туралы зерттеп, нәтиже ұсыну"]),
    ("Қандай суперкүш саған жақын?", ["Кез келген технологияны жедел түсіну", "Кез келгенді логика мен сөзбен сендіру", "Бір ұстасамен кез келген ауруды жазу", "Миллиондарды толқытатын өнер жасау"]),
    ("Қиын мәселені қалай шешесің?", ["Қадамдарға бөліп, жоспар жазамын", "Адамдармен сөйлесіп, пікір жинаймын", "Шешім қабылдамас бұрын тереңдей зерттеймін", "Идея жинаймын және жаңа нәрселерді сынаймын"]),
    ("Қандай кино жанрын жақсы көресің?", ["ЖИ мен технология туралы ғылыми фантастика", "Сот драмалары мен саяси триллерлер", "Медициналық сериалдар мен деректі фильмдер", "Бизнес пен стартап туралы хикаялар"]),
    ("Климат өзгерісі туралы деректерді көресің. Алғашқы ойың?", ["ЖИ мұны қалай шеше алады?", "Үкіметтерді мәжбүр ете алатын заңдар қандай?", "Бұл адамдардың психикалық денсаулығына қалай әсер етеді?", "Хабардарлықты арттыру науқанын жасағым келеді"]),
    ("Жұмыс ортаң қандай болса жөн?", ["Тыныш, құлаққапта, терең шоғырлану", "Келіссөз бөлмелері, командалық жұмыс", "Аурухана, зертхана — адамдарға көмек", "Шығармашылық студия, мидан шауып ойлау"]),
    ("Өзіңнен нені мақтан тұтасың?", ["Басқалар тастап кеткен техникалық мәселелерді шешемін", "Адамдарды түсінемін және олардың сезімін тыңдаймын", "Нәрселерді әдемі және мағыналы етемін", "Ұйымдастырамын, басқарамын және нәтижеге жетемін"]),
    ("Мүмкіндік болса, күн сайын не жасар едің?", ["Нөлден жаңа жоба кодтау", "Нарықты зерттеп, питч жазу", "Мектепте немесе қоғамда волонтерлық", "Фотографиялау, түсіру немесе анимация жасау"]),
    ("Сандар мен статистикаға қалай қарайсың?", ["Жақсы көремін — паттерндер мен деректер қызықтырады", "Қаржыға қажет болса жарайды", "Сандан гөрі адамдармен жұмыс жасауды қалаймын", "Денсаулық пен биологияға байланысты болса ғана"]),
    ("Үлкен қолданбада осалдық таптың. Не жасайсың?", ["Жауапкершілікпен хабарлаймын — бұл қызықты!", "Заңдық және этикалық аспектілерді ойлаймын", "Пайдаланушы құпиялылығы туралы мақала жазамын", "Шынымды айтсам — өтіп кетемін, бұл маған емес"]),
    ("Болашақта қандай рол саған ұқсайды?", ["Технологиялық компанияда ЖИ зерттеушісі", "Хирург немесе мамандандырылған дәрігер", "Халықаралық адам құқықтары заңгері", "Дизайн агенттігінде арт-директор"]),
    ("Қазір дүниеде бір нәрсені өзгерте алсаң, ол не болар еді?", ["Сапалы білімді барлығына қолжетімді ету", "Денсаулық сақтаудағы теңсіздікті шешу", "ЖИ арқылы кедейлік пен аштықпен күресу", "Әділетсіз заңдарды реформалау"]),
    ("Қандай құралды меңгергің келеді?", ["Қолданбалар жасауға Python немесе JavaScript", "Дизайнға Figma немесе Adobe", "Заңдық деректер базалары мен прецеденттер", "Excel және қаржылық модельдеу"]),
    ("Ойын-сауық үшін қандай кітап оқыр едің?", ["Ғалым немесе өнертапқыштың өмірбаяны", "Адам мінезі туралы психология кітабы", "Стартап негізін қалаушының хикаясы", "Графикалық роман немесе өнер тарихы"]),
    ("Жергілікті мектеп көмек сұрайды. Не ұсынасың?", ["Балаларға кодтауды немесе робототехниканы үйретемін", "Театр немесе өнер шеберлік сыныбын өткіземін", "Экологиялық заң туралы лекция оқимын", "Медициналық тексеруде немесе алғашқы көмекте көмектесемін"]),
    ("Командада өзіңді қалай сезінесің?", ["Жақсы — мен барлығын байланыстырамын", "Жарайды, бірақ нақты лидер рөлімен жақсырақ", "Ортақ мақсаты бар шағын командада жақсырақ", "Шығармашылық тапсырмаларда жалғыз жұмыс жасауды қалаймын"]),
    ("Мектепте қандай пән ең жақсы ұнады?", ["Математика немесе информатика", "Биология немесе химия", "Тарих, әдебиет немесе қоғамтану", "Сурет, музыка немесе дизайн"]),
    ("Университеттен кейінгі бірінші жұмысың қай жерде болса арман?", ["Технологиялық стартапта", "Халықаралық заң фирмасында немесе ҮЕҰ-да", "Ауруханада немесе ғылыми-зерттеу институтында", "Халықаралық консалтинг компаниясында"]),
    ("Инвестиция үшін 1 миллион доллар болса, сен…", ["ЖИ немесе технологиялық стартапқа саламын", "Мектеп немесе білім беру платформасын ашамын", "Шалғай аймақта клиника саламын", "Шығармашылық агенттік немесе медиа компания ашамын"]),
    ("Өмірде не ең көп ашуландырады?", ["Тиімсіз жүйелер", "Маңайымдағы несправедливость", "Шығармашылықпен ойламайтын адамдар", "Қолдаусыз зардап шегетін адамдарды көру"]),
    ("Идеяларыңды қалай ұсынуды қалайсың?", ["Жұмыс жасайтын өнімнің тікелей демосын көрсету", "Дәлелдері бар толық жазбаша есеп", "Күшті дизайны бар визуалды презентация", "Эмоционалды байланыстыратын жеке хикая"]),
    ("Нақты адамдардың арасынан кімге таңдайсың?", ["Маск сияқты технологиялық визионер", "Ғалым немесе Нобель сыйлығының лауреаты", "Адам құқықтарын қорғаушы немесе заңгер", "Суретші немесе шығармашылық икона"]),
    ("Саған кез келген жерде жазғы тағылымдама ұсынады. Таңдайсың:", ["Google немесе Microsoft — әзірлеу командасы", "ДДҰ немесе Қызыл Крест", "БҰҰ немесе Amnesty International", "McKinsey, Goldman Sachs немесе стартап"]),
    ("Карьерадағы жоғары табыс саған қаншалықты маңызды?", ["Өте маңызды — қаржылық еркіндік қалаймын", "Маңызды, бірақ әлемге әсер ету маңыздырақ", "Ұнатқан ісіммен айналыссам, азырақ ала алам", "IT жақсы ақша төлейді және жұмысты жақсы көремін!"]),
    ("Жаңалықтарды оқыған кезде, қандай тақырыптар назарыңды аударады?", ["ЖИ жетістіктері немесе киберқауіпсіздік қауіптері", "Медициналық жаңалықтар мен эпидемиялар", "Сот шешімдері мен саяси пікірталастар", "Компания бірігулері мен стартап қаржыландыруы"]),
    ("3 жылда қандай дағдыны меңгергің келеді?", ["Машиналық оқыту және деректермен жұмыс", "Эмпатиялық кеңес беру мен психология", "UI/UX дизайн және визуалды повествование", "Халықаралық келіссөздер мен жария баяндамалар"]),
    ("Мұғалім қорытынды жоба жасауды сұрайды. Таңдайсың:", ["Жұмыс жасайтын веб-қолданба немесе бот жасау", "Комикс сызу немесе қысқа метражды фильм түсіру", "Әлеуметтік мәселе бойынша саяси ұсыныс жазу", "Бизнес-жоспармен мини-компания ашу"]),
    ("Болашақтан не қорқасың?", ["Технологиялар әлемінен артта қалу", "Жanlы мамандық жолын таңдау", "Дүниені жақсарту үшін жеткіліксіз жасау", "Шығармашылықсыз жұмысқа тұрып қалу"]),
]


def _build_questions(texts: list) -> List[dict]:
    values = ["a", "b", "c", "d"]
    result = []
    for i, (text, options) in enumerate(texts):
        result.append({
            "question_key": f"q{i + 1}",
            "text": text,
            "options": [
                {"value": values[j], "label": options[j], "weights": _W[i][j]}
                for j in range(4)
            ],
        })
    return result


QUESTIONS_BY_LANG = {
    "ru": _build_questions(_QUESTIONS_RU),
    "en": _build_questions(_QUESTIONS_EN),
    "kk": _build_questions(_QUESTIONS_KK),
}

QUESTIONS = QUESTIONS_BY_LANG["ru"]

SUMMARY_LABELS = {
    "ru": {
        "IT_ENGINEERING": "Технологии и инженерия", "DATA_AI": "Data Science и ИИ",
        "MEDICINE": "Медицина и здоровье", "BUSINESS": "Бизнес и финансы",
        "LAW": "Право и политика", "DESIGN_CREATIVE": "Дизайн и творчество",
        "SOCIAL_SCIENCES": "Социальные науки", "EDUCATION": "Образование",
    },
    "en": {
        "IT_ENGINEERING": "Technology & Engineering", "DATA_AI": "Data Science & AI",
        "MEDICINE": "Medicine & Health", "BUSINESS": "Business & Finance",
        "LAW": "Law & Policy", "DESIGN_CREATIVE": "Design & Creativity",
        "SOCIAL_SCIENCES": "Social Sciences", "EDUCATION": "Education",
    },
    "kk": {
        "IT_ENGINEERING": "Технология және инженерия", "DATA_AI": "Data Science және ЖИ",
        "MEDICINE": "Медицина және денсаулық", "BUSINESS": "Бизнес және қаржы",
        "LAW": "Заң және саясат", "DESIGN_CREATIVE": "Дизайн және шығармашылық",
        "SOCIAL_SCIENCES": "Әлеуметтік ғылымдар", "EDUCATION": "Білім беру",
    },
}

SUMMARY_TEMPLATES = {
    "ru": "Твои сильнейшие области: {top}. В топ-категории ты набрал {score:.0f}%. Ты процветаешь там, где аналитическое мышление сочетается с реальным влиянием на мир.",
    "en": "Your strongest interest areas are {top}. You scored {score:.0f}% in your top category. You thrive in environments that combine analytical thinking with real-world impact.",
    "kk": "Ең күшті салаларың: {top}. Топ санатыңда {score:.0f}% жинадың. Аналитикалық ойлау нақты ықпалмен үйлесетін ортада гүлденесің.",
}


class AssessmentService:
    @staticmethod
    def get_questions(lang: str = "ru") -> List[dict]:
        return QUESTIONS_BY_LANG.get(lang, QUESTIONS_BY_LANG["ru"])

    @staticmethod
    def calculate_scores(answers: Dict[str, str], lang: str = "ru") -> Tuple[Dict[str, float], Dict[str, float], List[str], List[str]]:
        raw_scores: Dict[str, float] = {cat: 0 for cat in CATEGORIES}
        questions = QUESTIONS_BY_LANG.get(lang, QUESTIONS_BY_LANG["ru"])

        for question in questions:
            qkey = question["question_key"]
            chosen_value = answers.get(qkey)
            if not chosen_value:
                continue
            for opt in question["options"]:
                if opt["value"] == chosen_value:
                    for cat, pts in opt["weights"].items():
                        raw_scores[cat] = raw_scores.get(cat, 0) + pts
                    break

        max_score = max(raw_scores.values()) if raw_scores.values() else 1
        if max_score == 0:
            max_score = 1
        normalized = {cat: round((score / max_score) * 100, 1) for cat, score in raw_scores.items()}
        top_categories = sorted(normalized, key=lambda c: normalized[c], reverse=True)[:3]
        recommended_majors: List[str] = []
        for cat in top_categories:
            recommended_majors.extend(MAJORS_MAP.get(cat, [])[:2])

        return raw_scores, normalized, top_categories, recommended_majors

    @staticmethod
    def build_profile_summary(top_categories: List[str], normalized_scores: Dict[str, float], lang: str = "ru") -> str:
        labels = SUMMARY_LABELS.get(lang, SUMMARY_LABELS["ru"])
        template = SUMMARY_TEMPLATES.get(lang, SUMMARY_TEMPLATES["ru"])
        top_names = ", ".join(labels.get(c, c) for c in top_categories[:3])
        score = normalized_scores.get(top_categories[0], 0) if top_categories else 0
        return template.format(top=top_names, score=score)

    @staticmethod
    def save_result(db: Session, user_id: int, answers: Dict[str, str], lang: str = "ru") -> AssessmentResult:
        raw_scores, normalized, top_cats, rec_majors = AssessmentService.calculate_scores(answers, lang)
        summary = AssessmentService.build_profile_summary(top_cats, normalized, lang)

        existing = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).first()
        if existing:
            existing.raw_scores = raw_scores
            existing.normalized_scores = normalized
            existing.top_categories = top_cats
            existing.recommended_majors = rec_majors
            existing.profile_summary = summary
            existing.answers = answers
            db.commit()
            db.refresh(existing)
            return existing

        result = AssessmentResult(
            user_id=user_id,
            raw_scores=raw_scores,
            normalized_scores=normalized,
            top_categories=top_cats,
            recommended_majors=rec_majors,
            profile_summary=summary,
            answers=answers,
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
