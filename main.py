from time import * 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fazer_login(driver, wait):

    driver.get("https://talkabit-z3eg.onrender.com/app/login")

    campo_login_id = wait.until(EC.presence_of_element_located((By.ID, "teamToken")))
    campo_login_id = driver.find_element(By.ID,"teamToken")
    campo_login_id.send_keys("MATRIX-KXGM6")

    campo_login_id = driver.find_element(By.ID,"password")
    campo_login_id.send_keys("talkabit")

    botao = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    botao.click()

def check_popup(driver, wait):

    check_pagina = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "topbar")))

    wait = WebDriverWait(driver, 2)

    try:
        popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "np-overlay")))

        botaofechar = driver.find_element(By.CSS_SELECTOR, ".np-overlay button")
        botaofechar.click()

    except TimeoutException:
        pass

def check_captcha(driver, wait):
    mensagem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "muted")))

    try:
        captcha = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))

        operacao = driver.find_element(By.TAG_NAME, "label").text
        operacao = operacao.replace("?", "").split(' ')
        op1 = int(operacao[2])
        op2 = int(operacao[4])

        if operacao[3] == '+':
            resultado = op1 + op2
        elif operacao[3] == '-':
            resultado = op1 - op2
        elif operacao[3] == '*' or operacao[3].lower() == 'x':
            resultado = op1 * op2
        elif operacao[3] == '/':
            resultado = op1 - op2

        resposta = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[inputmode='numeric']")))
        resposta.send_keys(str(resultado))

        botao = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        botao.click()
    except TimeoutException:
        pass

def procurar_infos(driver, wait):

    linhas = driver.find_elements(By.CSS_SELECTOR, "#resultados table tbody tr")

    for linha in linhas:

        dados = linha.find_elements(By.TAG_NAME, "td")

        status = linha.find_element(By.CSS_SELECTOR, ".badge").text

        if status == 'Autorizada':
            link = linha.find_element(By.CSS_SELECTOR, "a")
            link.click()
            infos = driver.find_elements(By.CSS_SELECTOR, "#card table tbody tr")

            chave = infos[1]
            chave = chave.find_element(By.CSS_SELECTOR, "td[data-chave]")

            valor = infos[5]
            valor = valor.find_element(By.CSS_SELECTOR, "td")

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5) #Driver espera no máximo 5 segundos

    fazer_login(driver, wait)

    check_popup(driver, wait)

    botao_busca = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    botao_busca.click()

    check_captcha(driver, wait)

    check_popup(driver, wait)
    sleep(5)

main()