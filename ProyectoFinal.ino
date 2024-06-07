#include <Servo.h>

class BrazoRobot {
  private:
    Servo servoBase;
    Servo servoHombro;
    Servo servoCodo;
    
    const int pinBase = 10;
    const int pinHombro = 11;
    const int pinCodo = 12;

  public:
    void configurar() {
      servoBase.attach(pinBase);
      servoHombro.attach(pinHombro);
      servoCodo.attach(pinCodo);
      
      Serial.begin(9600);
    }

    void bucle() {
      if (Serial.available() > 0) {
        String entrada = Serial.readStringUntil('\n');
        int primerIndiceComa = entrada.indexOf(',');
        int segundoIndiceComa = entrada.indexOf(',', primerIndiceComa + 1);

        if (primerIndiceComa != -1 && segundoIndiceComa != -1) {
          int anguloBase = entrada.substring(0, primerIndiceComa).toInt();
          int anguloHombro = entrada.substring(primerIndiceComa + 1, segundoIndiceComa).toInt();
          int anguloCodo = entrada.substring(segundoIndiceComa + 1).toInt();
          
          anguloBase = constrain(anguloBase, 0, 180);
          anguloHombro = constrain(anguloHombro, 15, 165);
          anguloCodo = constrain(anguloCodo, 0, 180);
          
          servoBase.write(anguloBase);
          servoHombro.write(anguloHombro);
          servoCodo.write(anguloCodo);
        } else {
          Serial.println("Error: Entrada malformada");
        }
      }
    }
};

BrazoRobot brazoRobot;

void setup() {
  brazoRobot.configurar();
}

void loop() {
  brazoRobot.bucle();
}
