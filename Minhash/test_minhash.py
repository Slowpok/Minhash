import String_methods
import Minhash

str1 = "aksjdnajksd£4%^&nlkas dвыаваывава"
str2 = "aksjdnajksdnlkasd выаваывава"

num1, str1 = String_methods.string_in_ordnung(str1, True)
num2, str2 = String_methods.string_in_ordnung(str2, True)

# Minhash.strings_comparison_with_numbers(str1, str2, num1, num2)

str1 = String_methods.string_in_ordnung(str1)
str2 = String_methods.string_in_ordnung(str2)

# Minhash.strings_comparison(str1, str2)

dict_for_conc = []
dict_for_conc.append("Дифманометр-напоромер ДНМПКр-100-60 кгс/м2-2,5")
dict_for_conc.append("Дифманометр-напоромер ДНМПКр-100-60 кгс/м2-2,5")
dict_for_conc.append("напоромезная Дифманометр- ДНМПКр-100 кгс/м2-2,5")
dict_for_conc.append("Дифманометр-напоромез ДНМПКр-100 кгс/м2-2,5")
dict_for_conc.append("Дифманометр тягомер ДТмМПКр-100-160 кгс/м2-2,5")
dict_for_conc.append("Дифманометр-тягонапоромер ДТНМПКР-100-500 кгс/м2")
dict_for_conc.append("Дифманометр-напоромер ДНМПКР-100 с пределом измерения 2,5 кПа (250 кгс/м2)")
dict_for_conc.append("Дифманометр-напоромер ДНМПКР-100 с пределом измерения 4,0 кПа (400 кгс/м2)")
dict_for_conc.append("Дифманометр-тягомер ДТММПКР-100 с пределом измерения 1,6 кПа (160 кгс/м2)")
dict_for_conc.append("Универсальный измерительный прибор для проверки милливольтметров, приборов показывающих, подгонки сопротивления внешней лапки и прочее Р-4833")
dict_for_conc.append("Фильтр 1 2ФЗВ 80/4–2,5")
dict_for_conc.append("Фильтр конденсата сдвоенный с контрфланцами DN65")
dict_for_conc.append("Фильтр конденсата сдвоенный с контрфланцами DN65")
dict_for_conc.append("Кольцо")
dict_for_conc.append("Патрон фильтрующий")
dict_for_conc.append("Прокладка")
dict_for_conc.append("Прокладка")
dict_for_conc.append("Клапан дроссельный штуцерный угловой 20-6,3(63,0)кор.ст")
dict_for_conc.append("Клапан проходной самозакрывающийся муфтовый бронзовый 15-0,3 (3,0)")
dict_for_conc.append("Поплавок")
dict_for_conc.append("Кольцо")
dict_for_conc.append("Кольцо поршневое")
dict_for_conc.append("Клапан редукционный для пара")
dict_for_conc.append("Клапан дроссельный проходной бесфланцевый 2-65-1,0(10,0)бр")
dict_for_conc.append("Клапан дроссельный проходной бесфланцевый 2-65-1,0(10,0)лат")
dict_for_conc.append("Клапан дроссельный штуцерный угловой 10-6,3(63,0)кор.ст")
dict_for_conc.append("Клапан дроссельный штуцерный угловой 10-6,3(63,0)кор.ст")
dict_for_conc.append("Шайба 85,5-5,1-2,0")
dict_for_conc.append("Фильтр гидравлический ФГС-20-1 ОМ2")
dict_for_conc.append("Наполнитель – кокс")
dict_for_conc.append("Элемент фильтрующий")
dict_for_conc.append("Кольцо")
dict_for_conc.append("Кольцо")
dict_for_conc.append("Патрон фильтрующий")
dict_for_conc.append("Фильтр для конденсата фланцевый Dy 25 Рр 4")

list_in_ordnund = []
for i in dict_for_conc:
    list_in_ordnund.append(String_methods.string_in_ordnung(i))

prprprpr = Minhash.mass_string_comparison(list_in_ordnund)

print("Сравниваем с " + dict_for_conc[0])

for key, value in prprprpr.items():
    print(dict_for_conc[key], " ", value)

