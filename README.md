Servidor feito em python, usando a lib Flask.

Este projeto é apenas um servidor simples e funcional de login/signin feito com Flask, SQLite, hashing (Segurança nas passwords), verificação de email e um pequeno "Sobre mim".
Inclui páginas de login, registo, logout, página principal e envio de dicas personalizadas.

Funcionalidades do servidor

#=======================================================================

Autenticação de utilizador

Registo com:

	Username - (Unico)
  	Email válido e não duplicado - (Sem confirmação por email)
  	Password segura - ( 8+ caracteres, com no minimo 1 letra e 1 numero)
    
Login com verificação de hash - (como as passes são guardadas em hash com werkzeug.security, implementei uma verificação de pass com a mesma.)

Logout- (Sai da sessão e redireciona para o login)
#=======================================================================

Base de Dados usada:

    SQLite3
		
    Tabela users com:
        id - ( o mesmo do username)
        hashpass - ( é password protegida)
        email
        tips - (campo opcional para sugestões do que adicionar no servidor, feito na rota "Aboutme")
#=======================================================================

Como é feita a validação de email?

Usa email_validator para garantir que o email existe e é válido, mas não confirmado por email.
#=======================================================================

Qual a segurança?

  Passwords nunca são guardadas em texto simples, pois isso leva a falhas de segurança, sejam elas por roubo de dados, ou mesmo por o Owner ter acesso aos dados.
  Em vez disso usamos a tecnica "Hashing" com generate_password_hash, que gera um codigo para a password fornecida.
  Assim, nem o owner nem ninguem teria acesso ás passwords mesmo com falha de segurança.
  Sessões protegidas com secret_key como assinatura digital, para evitar mudanças entre o servidor e o user
	
#=======================================================================

Sistema de "Tips" (Dicas)
  Os utilizadores logados podem enviar dicas do que adicionar no servidor na rota "aboutme".
	
  As dicas são guardadas na base de dados juntas com os dados do utilizador, escolhi usar 1 por utilizador para não haver "spam" de tips.
