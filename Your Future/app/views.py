import base64
from datetime import timedelta
from django.utils import timezone
import io
from pyexpat.errors import messages
from django.template import loader
from django.db.models import Sum
from matplotlib import pyplot as plt
from app.form_cadastro_curso import FormCadastroCurso
from app.form_cadastro_user import FormCadastroUser
from app.form_compra_curso import FormCompraCurso
from app.redefinir_senha_user import RedefinirSenhaUser
from app.form_login import FormLogin
from app.form_foto import FormFoto
from app.models import Curso, Usuario, Foto, Vendas
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    sessao = 'email' in request.session
    return render(request, 'index.html', {'sessao': sessao})  

def contato(request):
    return render(request, 'contato.html')

def pagamento(request):
    return render(request, 'contato.html')
 
def cadastrar_user(request):
    novo_user = FormCadastroUser(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if novo_user.is_valid():
            email = novo_user.cleaned_data['email']

            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "E-mail já está sendo utilizado!")
            else:
                usuario = Usuario(
                    nome=novo_user.cleaned_data['nome'],
                    email=email,
                    senha=make_password(novo_user.cleaned_data['senha']),
                    foto=novo_user.cleaned_data['foto'],
                )
                usuario.save() 
                messages.success(request, "Usuário cadastrado com sucesso!")
                return redirect('index')  
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    
    context = {
        'form': novo_user  
    }
    return render(request, 'cadastro.html', context)

def exibir_user(request):
    if not request.session.get('email'):
        messages.error(request, "Você precisa estar logado para acessar a lista de usuários")
        return redirect('index')
    users = Usuario.objects.all()  
    return render(request, 'usuarios.html', {'users': users})

def cadastrar_curso(request):
    if not request.session.get('email'):
        messages.error(request, "Você precisa estar logado para cadastrar um curso!")
        return redirect('index')

    novo_curso = FormCadastroCurso(request.POST or None, request.FILES or None)
    if request.POST:
        if novo_curso.is_valid():
            novo_curso.save()
            messages.success(request, 'Curso Cadastrado com Sucesso!')
            return redirect('index')
    
    context = {
        'form' : novo_curso
    }
    
    return render(request, 'cadastro_curso.html', context)

def exibir_curso(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos.html', {'cursos': cursos})

def fazer_login(request):
    formLogin = FormLogin(request.POST or None)
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session.set_expiry(timedelta(seconds=1000))
                request.session['email'] = email
                messages.success(request, 'Login bem-sucedido!')
                return redirect('dashboard')
            else:
                messages.error(request, "Senha incorreta.")
        except Usuario.DoesNotExist: 
            messages.error(request, "Usuário não encontrado.")
    context = {
        'form': formLogin
    }
    return render(request, 'login.html', context)

def dashboard(request):
    if not request.session.get('email'):
        messages.error(request, "Você precisa estar logado para acessar o dashboard")
        return redirect('index')
    try:
        email = request.session.get('email')
        usuario_logado = Usuario.objects.get(email = email)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado")
        return redirect('form_login')
    context = {
        'dados':[usuario_logado]
    }
    return render(request, 'dashboard.html', context)

def editar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id = id_usuario)
    form = FormCadastroUser(request.POST or None, instance=usuario)
    if request.POST :
        if form.is_valid():
            form.save()
            return redirect('exibir_user')
    context = {
        'form' : form
    }
    return render(request, 'editar_usuario.html', context)
    

def excluir_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id = id_usuario)
    usuario.delete()
    return redirect('exibir_user')

def redefinir_senha(request):
    email = request.session['email']
    usuario = Usuario.objects.get(email=email)
    
    senha_atual = request.POST.get('senha_atual')
    nova_senha = request.POST.get('nova_senha')
    confirmacao_senha = request.POST.get('confirmacao_senha')

    if not check_password(senha_atual, usuario.senha):
        messages.error(request, 'A senha atual está incorreta.')
        return render(request, 'redefinir_senha.html')

    if nova_senha != confirmacao_senha:
        messages.error(request, 'As senhas não coincidem.')
        return render(request, 'redefinir_senha.html')

    usuario.senha = make_password(nova_senha)
    usuario.save()
    messages.success(request, 'Senha alterada com sucesso!')
    return redirect('dashboard')
    
def add_foto(request):
    if request.POST:
        form = FormFoto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else: 
        form = FormFoto()
    return render(request, 'add_foto.html', {'form': form})
    
def galeria(request):
    if not request.session.get('email'):
        messages.error(request, "Você precisa estar logado para acessar a lista de usuários")
        return redirect('index')
    fotos = Foto.objects.all()
    usuarios = Usuario.objects.all()
    cursos = Curso.objects.all()

    context ={
        'usuarios_fotos': fotos,
        'cursos_fotos': usuarios,
        'fotos_fotos': cursos,
    }
    return render(request, 'galeria.html', context)

def comprar_curso(request, curso_id):
    if not request.session.get('email'):
        messages.error(request, "Você precisa estar logado para realizar uma compra.")
        return redirect('login') 

    curso = get_object_or_404(Curso, id=curso_id)
    usuario_email = request.session.get('email')
    usuario = get_object_or_404(Usuario, email=usuario_email)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        if curso.quantidade_estoque >= quantidade:
            curso.quantidade_estoque -= quantidade
            curso.save()
            Vendas.objects.create(
                usuario=usuario,
                curso=curso,
                quantidade=quantidade
            )
            messages.success(request, f"Compra realizada com sucesso! Você comprou {quantidade}x {curso.nome}.")
            return redirect('exibir_curso') 
        else:
            messages.error(request, "Estoque insuficiente para a quantidade solicitada.")
    else:
        form = FormCompraCurso(initial={'curso': curso, 'quantidade': 1})
    return render(request, 'comprar_curso.html', {'form': form, 'curso': curso})

def relatorio_vendas(request):
    if not request.session.get('email'):
        messages.error(request, "Você precisa estar logado para acessar o relatório.")
        return redirect('login') 

    hoje = timezone.now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    vendas_gerais = Vendas.objects.filter(data_compra__month=mes_atual, data_compra__year=ano_atual).values('data_compra__month').annotate(total_vendas=Sum('quantidade'))

    meses = [venda['data_compra__month'] for venda in vendas_gerais]
    total_vendas = [venda['total_vendas'] for venda in vendas_gerais]

    fig_gerais, ax_gerais = plt.subplots()
    ax_gerais.bar(meses, total_vendas, label="Vendas Totais", color='blue')
    ax_gerais.set_title("Vendas Gerais Mensais")
    ax_gerais.set_xlabel("Mês")
    ax_gerais.set_ylabel("Total de Vendas")
    ax_gerais.legend()

    buf_gerais = io.BytesIO()
    fig_gerais.savefig(buf_gerais, format='png')
    buf_gerais.seek(0)
    img_gerais = base64.b64encode(buf_gerais.getvalue()).decode('utf-8')

    vendas_por_curso = Vendas.objects.filter(data_compra__month=mes_atual, data_compra__year=ano_atual).values('curso__nome').annotate(total_vendas=Sum('quantidade'))

    cursos = [venda['curso__nome'] for venda in vendas_por_curso]
    vendas_por_curso_vals = [venda['total_vendas'] for venda in vendas_por_curso]

    fig_curso, ax_curso = plt.subplots()
    ax_curso.bar(cursos, vendas_por_curso_vals, color='green')
    ax_curso.set_title("Vendas por Curso")
    ax_curso.set_xlabel("Curso")
    ax_curso.set_ylabel("Total de Vendas")

    buf_curso = io.BytesIO()
    fig_curso.savefig(buf_curso, format='png')
    buf_curso.seek(0)
    img_curso = base64.b64encode(buf_curso.getvalue()).decode('utf-8')

    context = {
        'vendas_gerais': vendas_gerais,
        'vendas_por_curso': vendas_por_curso,
        'img_gerais': img_gerais,
        'img_curso': img_curso,
    }
    return render(request, 'relatorio_vendas.html', context)

def logout (request):
    if request.session.get('email'):
        request.session.flush()
        messages.success(request, "Você saiu da sua conta com sucesso!")
    else:
        messages.info(request, "Você já está deslogado.")
    return redirect('index')
