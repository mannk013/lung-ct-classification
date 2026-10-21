from idc_index import IDCClient

client = IDCClient()
client.download_from_selection(
    downloadDir="data/raw",
    collection_id="lung_pet_ct_dx",
    patientId="Lung_Dx-A0001",
)