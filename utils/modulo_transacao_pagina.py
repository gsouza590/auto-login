import time

from selenium.common import NoSuchElementException


def transicao_paginas(navegador):
    time.sleep(3)
    navegador.get("https://projetos.dpf.gov.br/siseg/principal.php")
    navegador.find_element('xpath', '//*[@id="226"]/img').click()

    janelas = navegador.window_handles
    navegador.switch_to.window(janelas[1])
    time.sleep(5)
    navegador.get(navegador.current_url)
    try:
        navegador.find_element('xpath', '//*[@id="formConteudo:j_id280:opRelatorio:0:j_id320:0:j_id322"]').click()
    except NoSuchElementException as e:
        print(f"Erro do servidor ao logar, tente novamente {e}")