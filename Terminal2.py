import os

comandos_utilizados = [] #criação do vetor para listar os comandos utilizados (válidos) [vou validar mais pra frente]

print("Terminal de Linux")

i = 0
command_err = False # a condição de erro no comando começa falsa pois sem comando, não tem como dar erro, certo?
while True: #O programa entra em um loop infinito, onde o usuário pode inserir comandos repetidamente.
    command = input("osh> ")

    pid = os.fork() #utilização do fork para criar um processo filho.

    if pid == 0:
        args = command.split()
        
        if args[0] == "exit":
            print("Loop finalizado.") #comando exit pra quebrar o loop infinito.
            break

        if args[0] == "history":
            for index, valor in enumerate(reversed(comandos_utilizados), start=1):
                if valor != "history":
                    print(f"{len(comandos_utilizados) - index + 1} {valor}")
            os._exit(0)  # Encerra o processo filho sem mensagem de erro (Tem que encerrar para voltar pro processo pai e aguradar o prox comando) nesse caso fiz um if só pro history pois é um comando do simulador e não do terminal pelo que entendi.

        if not command.startswith("!") and args[0] != "history": #aqui é a validação dos comandos. Só entra pra validação caso não comece com '!' e o primeiro argumento do comando não seja history (que ia dar erro por ser um comando do simulador e não do terminal do Linux).
            try:
                os.execvp(args[0], args) #Aqui ele tenta executar o comando, se der certo, blz.
            except FileNotFoundError:
                print(f"Comando não encontrado: {args[0]}") #Exceção para erro. Caso não encontre o comando, a variável erro passa a ser True prara que lá na linha de verificação dessa variável ele não faça adicione o comando na lista do histórico.
                command_err = True
                os._exit(1)  # Encerra o processo filho sem mensagem de erro (Tem que encerrar para voltar pro processo pai e aguradar o prox comando)


    #Aqui o processo pai abaixo é dentificado por pid > 0. Dentro desse if o código aguarda que o processo filho termine usando os.wait(). Após isso, ele faz a verificação dao código de saída do processo filho com a função os.WEXITSTATUS(status). Se o código de saída for 1, então é porque ocorreu um erro ao executar o comando no processo filho. Então eu adicionei um continue para evitar adicionar o comando inválido à lista de comandos utilizados.

    elif pid > 0:
        _, status = os.wait()
        if os.WEXITSTATUS(status) == 1:
            continue  # Evita adicionar comandos inválidos à lista

    else:
        print("Houve uma falha na criação do processo.")


    #Comandos especiais. Aqui é um comando do pŕoprio simulador. !! retorna último comando válido, e ! com numeração, retorna um comando específico da lista do histórico.
    if command == "!!":
        print(comandos_utilizados[-1] if comandos_utilizados else "Nenhum comando correspondente no histórico.") #if dentro do print é possível

    elif command.startswith("!"): #Fiz a verificação do comando '!!' pa ficar mais fácil, aqui consdiera os outros começando por um '!' e um número.
        try:
            num = int(command[1:])
            if num == 1 and comandos_utilizados:
                print(comandos_utilizados[0])
            elif 1 <= num <= len(comandos_utilizados):
                print(comandos_utilizados[num - 1])
            else:
                print("Número de histórico inválido")
        except ValueError: #tratamento de erro para um erro específico, no caso um valor, ou seja, se for uma posição que não tem no vetor.
            print("Comando de histórico inválido")

    elif(command_err == False and command != 'history' and not command.startswith("!")): #esse else if é uma condição para adicionar a lista do histórico somente comando válidos, no caso, ele não contabiliza se deu erro no comando, se for o comando history, ou começar por '!', pois são comandos do simulador e não do terminal.
        comandos_utilizados.append(command)
        command_err = False #volta a ser Falso depois que é adc na lista porque vai repetir o processo.
