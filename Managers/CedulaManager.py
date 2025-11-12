def comprobarCedula(cedula_str: str):
    if len(cedula_str) != 10:
        return False
    
    cedula = [int(d) for d in cedula_str]
    modified_cedula = cedula[0:9]
    processed_digits = []
    for i, caracter in enumerate(modified_cedula):
        if i%2 == 0:
            processed_digit = caracter*2
            if processed_digit >9:
                processed_digit-=9
            processed_digits.append(processed_digit)
        else:
            processed_digits.append(caracter)
    
    processed_digits_sum = sum(processed_digits)
    sum_mod = processed_digits_sum%10
    digito_calculado = 0 if sum_mod == 0 else 10 - sum_mod
    print(f"digito calculado: {digito_calculado}")
    
    if (digito_calculado) == cedula[9]:
        return True
    else:
        return False
