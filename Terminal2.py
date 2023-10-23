import os

comandos_utilizados = [] #criação do vetor para listar os comandos utilizados (válidos) [vou validar mais pra frente]

print("Terminal de Linux")

rodando = True
command2 = ''
while rodando: #O programa entra em um loop infinito, onde o usuário pode inserir comandos repetidamente.
    command_err = False # a condição de erro no comando começa falsa pois sem comando, não tem como dar erro, certo?

    if command2 == '':
        command = input("osh> ")
    
    else:
        command = command2
        command2 = ''
    
    args = command.split() #O comando é separado em argumentos, já que pode ter mais de um. Esse argumentos serão armazenados no vetor args. Os argumentos serão lidos na ordem das palavras da String.

    if args[0] == "exit" and len(args) ==1:
        print("Loop finalizado.")
        rodando = False
        continue


    elif args[0] == "history" and len(args) ==1: #Nesse caso, se o primeiro argumento (palavra) do comando inserido for history, automaticamente ele vai reconhecer como comando history dos últimos comandos válidos enviados. Se por um acaso o comando consta com mais de um argumento além do history, o comando não é reconhecido.
            for index, valor in enumerate(reversed(comandos_utilizados), start=1):
                if valor != "history":
                    print(f"{len(comandos_utilizados) - index + 1} {valor}")
    
    if(command_err == False and command != 'history' and not command.startswith("!")):
        pid = os.fork() #utilização do fork para criar um processo filho.

    if pid == 0: #Nesse caso entramos dentro do contexto do processo filho, onde os comandos serão executados;

        if not command.startswith("!") and args[0] != "history": #aqui é a validação dos comandos. Só entra pra validação caso não comece com '!' e o primeiro argumento do comando não seja history (que ia dar erro por ser um comando do simulador e não do terminal do Linux).
            try:
                os.execvp(args[0], args) #Aqui ele tenta executar o comando, se der certo, blz, segue o código.
            except FileNotFoundError:
                print(f"Comando não encontrado: {args[0]}") #Exceção para erro. Caso não encontre o comando, a variável erro passa a ser True prara que lá na linha de verificação dessa variável ele não faça adicione o comando na lista do histórico.
                command_err = True
            os._exit(0)  # Encerra o processo filho sem mensagem de erro (Tem que encerrar para voltar pro processo pai e aguradar o prox comando)
            
    #Aqui o processo pai abaixo é dentificado por pid > 0. Dentro desse if o código aguarda que o processo filho termine usando os.wait(). Após isso, ele faz a verificação dao código de saída do processo filho com a função os.WEXITSTATUS(status). Se o código de saída for 1, então é porque ocorreu um erro ao executar o comando no processo filho. Então eu adicionei um continue para evitar adicionar o comando inválido à lista de comandos utilizados.

    elif pid > 0 and command_err == False and command != 'history' and not command.startswith("!"):
        _, status = os.wait() # "_" é usado para descartar o valor de retorno que os.wait() retorna, que seria o ID do processo que terminou. Nesse caso queremos apenas o satus de saída do processo filho, retornado para a variável status. Nesse caso, ele espera a certificação do status para indicar que o processo filho acabou.
        command2 = ''
        if os.WEXITSTATUS(status) == 1 and rodando==True:
            continue  # Evita adicionar comandos inválidos à lista, pois se caso seja 1 significa que o retorno deu algum tipo de erro.



    #Comandos especiais. Aqui é um comando do pŕoprio simulador. !! retorna último comando válido, e ! com numeração, retorna um comando específico da lista do histórico.
    if command == "!!":
        if len(comandos_utilizados)>0:
            command2 = comandos_utilizados[len(comandos_utilizados)-1]
        else:
            print("Nenhum comando correspondente no histórico.")

    elif command.startswith("!"): #Fiz a verificação do comando '!!' pa ficar mais fácil, aqui consdiera os outros começando por um '!' e um número.
        try:
            num = int(command[1:])
            if num == 1 and comandos_utilizados:
                command2 = comandos_utilizados[0]
            elif 1 <= num <= len(comandos_utilizados):
                command2 = comandos_utilizados[num - 1]
            else:
                print("Número de histórico inválido")
        except ValueError: #tratamento de erro para um erro específico, no caso um valor, ou seja, se for uma posição que não tem no vetor.
            print("Comando de histórico inválido")

    elif(command_err == False and command != 'history' and not command.startswith("!")): #esse else if é uma condição para adicionar a lista do histórico somente comando válidos, no caso, ele não contabiliza se deu erro no comando, se for o comando history, ou começar por '!', pois são comandos do simulador e não do terminal.
        comandos_utilizados.append(command)