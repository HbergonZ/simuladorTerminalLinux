import os

comandos_utilizados = [] #criação de um vetor para armazenas os comandos válidos utilizados (no caso vai ser  histórico).

print("Terminal de Linux") #título do terminal (acho que não precisa)

command2 = '' #command2 é uma variável que armazena um comando da lista dos utilizados ou o último comando. Por isso ela inicia nula.
rodando = True #rodando é a variável que mantem o loop do programa, armazenando True até a utilização do comando exit().

while rodando: #início do loop
    if command2 == '': #inicialmente uma verificação se foi usado alguma chamada de um comando da lista de comando utilizados (inicialmente não tem nenhum).
        command = input("osh> ")
    else:
        command = command2 #caso aja, o comando utilizado passa a ser o comando solicitado da lista.
        command2 = '' #e o command2 volta a ser nula para que não fique infinitamente no mesmo comando.

    args = command.split() #aqui há uma divisão da string para fazer a verificação do comando


    #Abaixo eu optamos por verificar se o comando utilizado trata-se inicialmente de um comando so simulador e não do terminal, e só por fim, tenta executar o comando no terminal.
    if command == "!!":  #caso o comando seja para executar o último comando utilizado da lista
        if len(comandos_utilizados) > 0: #verifica se a lista possui algum comando já executado, caso sim, executa o último utilizado.
            command2 = comandos_utilizados[len(comandos_utilizados) - 1] #aqui a variavel command2 recebe o último comando.
        else:
            print("Nenhum comando correspondente no histórico.") #caso nãõ haja pelo menos um comando na lista, o usuário é avisado.
            
    elif command.startswith("!"): #caso a condição de cima nãõ seja atentida, verifica se o comando inicia com "!"
        try: #aqui tenta executar o comando ex !1 !2 !3...
            num = int(command[1:]) #aqui tenta identificar o número após a exclamação
            if num == 1 and comandos_utilizados:#se for 1, o comando utilizado é o primeiro da lista
                command2 = comandos_utilizados[0]
            elif 1 <= num <= len(comandos_utilizados): #se tiver entre 1 e o tamanho da lista o comando executa o comando da posição indicada.
                command2 = comandos_utilizados[num - 1]
            else:
                print("Número de histórico inválido") #caso contrário retorna numéro inválido.
        except ValueError:
            print("Comando de histórico inválido") #caso de erro no comando, retorna comando inválido.

    elif args[0] == "exit" and len(args) == 1: #caso o comando seja exit, exibe print finalizado e a variável do loop passa a ser False. Após isso, tem um continue que ignora o que vem após e volta para o início do loop para fazer a verificação do rodando.
        print("Loop finalizado.")
        rodando = False
        continue

    elif args[0] == "history" and len(args) == 1: #caso o comando seja history, exibe a lista de comandos utilizados, sendo enumeradas reverso (de baixo pra cima) iniciando em 1.
        for index, valor in enumerate(reversed(comandos_utilizados), start=1):
            if valor != "history": #isso aqui é para não contabilizar o comando history na lista da comando utilizados, pois nãõ é um comando do terminal.
                print(f"{len(comandos_utilizados) - index + 1}) {valor}")

    else:
        pid = os.fork() #por fim, se nenhuma verificação acima for atendida, cria-se o processo filho para tentar executar o comando no terminal do linux.
        if pid == 0: #Nesse caso entramos dentro do contexto do processo filho, onde os comandos serão executados;
            try:
                os.execvp(args[0], args) #nessa linha tenta executar o comando no terminal do linux.
            except FileNotFoundError: #Caso não tenha sido possível executar, exibe a mensagem avisando o usuário e encerra o processo filho retornando 1.
                print(f"Comando não encontrado: {args[0]}")
                os._exit(1) #encerra o processo filho e retorna 1

        if pid > 0: #Nesse caso voltamos para o processo pai, onde será verificado se o processo filho terminou;
            _, status = os.wait() #aguarda o processo filho terminar
            #command2 = ''
            if os.WEXITSTATUS(status) == 1 and rodando == True: #verifica se o retorno após o processo filho ser finalizado é 1, ou seja, se deu erro, caso sim, utiliza-se o continue para voltar para o início do loop e ignorar a parte abaixo do continue.
                continue

    if args[0] != "history" and not command.startswith("!"): #caso o comando não tenha sido inválido, o código chega nessa verificaç~ao onde se o comando utilizado nãõ foi o history e nem começa com exclamação, ele é adicionado ao vetor de comandos utilizados.
        comandos_utilizados.append(command)
