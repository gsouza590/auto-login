import time


def transicao_paginas(navegador):
    time.sleep(3)
    navegador.get("https://projetos.dpf.gov.br/siseg/principal.php")
    navegador.find_element('xpath', '//*[@id="226"]/img').click()

    janelas = navegador.window_handles
    navegador.switch_to.window(janelas[1])
    time.sleep(3)
    navegador.get(navegador.current_url)
    navegador.find_element('xpath', '//*[@id="formConteudo:j_id274:opRelatorio:0:j_id314:0:j_id316"]').click()
