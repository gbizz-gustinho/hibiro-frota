{% extends "base_app.html" %}
{% block title %}Financeiro - Hibiro Elite{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <div class="bg-white dark:bg-slate-800 rounded-3xl shadow-xl overflow-hidden border border-slate-200 dark:border-slate-700">
        <div class="bg-blue-600 p-6 flex items-center gap-4">
            <i class="fa-solid fa-building text-white text-2xl"></i>
            <h3 class="text-white font-black uppercase tracking-tighter">Configurações da Empresa</h3>
        </div>
        <div class="p-8">
            <p class="text-slate-500 font-bold uppercase text-xs">Dados de Faturamento e Identificação</p>
            <hr class="my-4 border-slate-100 dark:border-slate-700">
            <div class="py-10 text-center border-2 border-dashed border-slate-200 rounded-2xl">
                <i class="fa-solid fa-screwdriver-wrench text-slate-300 text-4xl mb-4"></i>
                <p class="text-slate-400 font-black uppercase text-[10px]">Módulo de Perfil em Manutenção</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}