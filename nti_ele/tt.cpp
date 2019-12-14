// НАСТРОЙКИ: ИСПОЛЬЗОВАТЬ, НО НЕ ТРОГАТЬ! ------------------------

// ВНИМАНИЕ!!!  В эти переменные "магически" попадают значения, введенные из входного потока,
// в тестах они могут меняться. Вам НЕ НАДО устанавливать в них никакие начальные значения,
// а просто использовать эти переменные в программе там, где это подходит по смыслу!

int PIN_BEEP; // каким пином мигаем
int DOT_TIME; // Длительность импульса "точка", в ms
// ------------------------------------

// ----------------------ВАШ КОД ЗДЕСЬ:

// #include <iostream>
// void delay(int a){
//     std::cout << "Delay: " << a << "\n";
// }
// void digitalWrite(int p, int a){
//     std::cout << "Write: " << a << "\n";
// }

int A[26][5]{
    {1, 2, 0, 0, 0}, //A
    {2, 1, 1, 1, 0}, //B
    {2, 1, 2, 1, 0}, //C
    {2, 1, 1, 0, 0}, //D
    {1, 0, 0, 0, 0}, //E
    {1, 1, 2, 1, 0}, //F

    {2, 2, 1, 0, 0},
    {1, 1, 1, 1, 0},
    {1, 1, 0, 0, 0},
    {1, 2, 2, 2, 0},
    {2, 1, 2, 0, 0}, //K

    {1, 2, 1, 1, 0}, //L
    {2, 2, 0, 0, 0}, //M
    {2, 1, 0, 0, 0}, //N
    {2, 2, 2, 0, 0},
    {1, 2, 2, 1, 0}, //P

    {2, 2, 1, 2, 0},
    {1, 2, 1, 0, 0},
    {1, 1, 1, 0, 0},
    {2, 0, 0, 0, 0}, // T
    {1, 1, 2, 0, 0},

    {1, 1, 1, 2, 0},
    {1, 2, 2, 0, 0},
    {2, 1, 1, 2, 0},
    {2, 1, 2, 2, 0},
    {2, 2, 1, 1, 0}

};

void do_b(char L, int p, int dt)
{
    int *l = A[(int)L - 65];
    // std::cout << L << "\n";
    for (int i = 0; i < 5; i++)
    {

        if (l[i] != 0)
        {
            if (l[i] == 1)
            {
                digitalWrite(p, 1);
                delay(dt);
                digitalWrite(p, 0);
                delay(dt);
            }
            else if (l[i] == 2)
            {
                digitalWrite(p, 1);
                delay(dt * 3);
                digitalWrite(p, 0);
                delay(dt);
            }
        }
    }
    delay(dt * 2);
}

void do_morze(char *ph, int l, int dt)
{
    for (int i = 0; i < l; i++)
    {
        char c = ph[i];
        if (c == ' ')
        {
            delay(dt * 4);
        }
        else
        {
            do_b(c, PIN_BEEP, dt);
        }
    }
}

void setup()
{
    // тут чего-то не хватает...
    pinMode(PIN_BEEP, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    if (Serial.available() > 0)
    {
        int l = 0;
        char buf[80];
        while (Serial.available() > 0)
        {
            char c = Serial.read();
            
            if (c == '.')
                break;
            buf[l] = c;
            l+=1;
        }
        do_morze(buf, l, DOT_TIME);
    }
}

// int main(){
//     loop();
//     return 0;
// }