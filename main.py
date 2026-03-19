from func import iniciar_sistema
from gui import *

if __name__ == "__main__":
    app = App()
    app.mainloop()
    try:
        iniciar_sistema()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário. Até logo!")
