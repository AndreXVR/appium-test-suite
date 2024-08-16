import alduin

driver = alduin.use()

el = driver.element(text="Battery")
print(el.text)
