🔐 Flask Login System
Um sistema simples e funcional de autenticação feito com Flask, SQLite, hashing seguro, validação de email e gestão de sessão.
Inclui páginas de login, registo, logout, página principal e envio de dicas personalizadas.

🚀 Funcionalidades
🔑 Autenticação Completa
Registo de utilizadores com:

Username único

Email válido e não duplicado

Password segura (mínimo 8 caracteres, letras e números)

Login com verificação de hash (werkzeug.security)

Logout com limpeza de sessão

🗄️ Base de Dados SQLite
Tabela users com:

id (username)

hashpass (password protegida)

email

tips (campo opcional para sugestões)

📬 Validação de Email
Usa email_validator para garantir que o email existe e é válido.

🔒 Segurança
Passwords nunca são guardadas em texto simples

Hashing com generate_password_hash

Sessões protegidas com secret_key

📝 Sistema de Dicas
Utilizadores autenticados podem enviar sugestões

As dicas são guardadas na base de dados
