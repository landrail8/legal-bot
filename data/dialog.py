
files_to_sending = {
  "Outsourcing_and_outstaffing": {
    "name": "Аутсорсинг и аутстаффинг",
    "filename": "Аутсорсинг и аутстаффинг.doc"
  },
  "Instruction_get_power_of_attorney": {
    "name": "Инструкция по получению доверенности",
    "filename": "Инструкция по получению доверенности.pdf"
  },
  "Prohibition_of_agency_labor": {
    "name": "Запрет заемного труда",
    "filename": "Запрет заемного труда.doc"
  },
  "Transportation_license": {
    "name": "Лицензия на перевозки",
    "filename": "Лицензия на перевозки.pdf"
  },
  "License_for_maintenance_of_fire_fighting_equipment": {
    "name": "Лицензия_на_обслуживание_противопожарного_оборудования",
    "filename": "Лицензия_на_обслуживание_противопожарного_оборудования.pdf"
  },
  "Signing_the_agreement_backdated": {
    "name": "Подписание_договора_задним_числом",
    "filename": "Подписание_договора_задним_числом.doc"
  },
  "Foreign_object_in_food": {
    "name": "Посторонний предмет в пище",
    "filename": "Посторонний предмет в пище.doc"
  },
  "Distinction_between_Lease_Agreements_and_Provision_of_Services": {
    "name": "Разграничение_договоров_аренды_и_оказания_услуг",
    "filename": "Разграничение_договоров_аренды_и_оказания_услуг.doc"
  },
  "Certificate_of_Insurance": {
    "name": "Сертификат о страховании",
    "filename": "Сертификат о страховании.pdf"
  },
  "Form_of_notification_about_occurrence_of_an_insured_event": {
    "name": "Форма_уведомления_о_наступлении_страхового_случая",
    "filename": "Форма_уведомления_о_наступлении_страхового_случая.doc"
  },
}




def get_path_file_to_send(filepath):
  return files_to_sending_dir + "/" + filepath

files_to_sending_dir = '/workdir/data/files' # '/var/lib/sqlite/data/files'
# def init_files_to_sending_dir():
#   # Check if the file exists
#   if not os.path.exists(files_to_sending_dir):
#     os.mkdir(files_to_sending_dir)
#     print("files_to_sending_dir created successfully.")
#   else:
#     print("files_to_sending_dir already exists.")
