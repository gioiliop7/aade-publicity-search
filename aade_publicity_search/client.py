import httpx
import xmltodict
from datetime import date
from .utils import validate_afm, get_key


class AadeClient:
    def __init__(self, username: str, password: str, afm: str = ""):
        self.username = username
        self.password = password
        self.afm = afm
        self.uri = "https://www1.gsis.gr/wsaade/RgWsPublic2/RgWsPublic2"

    @staticmethod
    def parse_response(xml: str) -> dict:
        data = xmltodict.parse(xml)

        envelope = get_key(data, "Envelope")
        body = get_key(envelope, "Body")
        response = next(iter(body.values()))
        result = get_key(response, "result")
        payload = get_key(result, "rg_ws_public2_result_rtType")

        error = payload.get("error_rec", {})
        basic = payload.get("basic_rec", {})
        firm_acts = payload.get("firm_act_tab", {}).get("item", [])

        if isinstance(firm_acts, dict):
            firm_acts = [firm_acts]

        return {
            "success": error.get("error_code") in (None, "0"),
            "error": {
                "code": error.get("error_code"),
                "description": error.get("error_descr"),
            },
            "basic": basic,
            "firm_activities": firm_acts,
        }

    async def get_vat_info(self, afm: str, as_on_date: date | None = None) -> dict:
        if not validate_afm(afm):
            raise ValueError("Invalid AFM")

        if not as_on_date:
            as_on_date = date.today()

        body = f"""<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope
 xmlns:env="http://www.w3.org/2003/05/soap-envelope"
 xmlns:ns1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
 xmlns:ns2="http://rgwspublic2/RgWsPublic2Service"
 xmlns:ns3="http://rgwspublic2/RgWsPublic2">
 <env:Header>
  <ns1:Security>
   <ns1:UsernameToken>
    <ns1:Username>{self.username}</ns1:Username>
    <ns1:Password>{self.password}</ns1:Password>
   </ns1:UsernameToken>
  </ns1:Security>
 </env:Header>
 <env:Body>
  <ns2:rgWsPublic2AfmMethod>
   <ns2:INPUT_REC>
    <ns3:afm_called_by>{self.afm}</ns3:afm_called_by>
    <ns3:afm_called_for>{afm}</ns3:afm_called_for>
    <ns3:as_on_date>{as_on_date.isoformat()}</ns3:as_on_date>
   </ns2:INPUT_REC>
  </ns2:rgWsPublic2AfmMethod>
 </env:Body>
</env:Envelope>
"""

        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(self.uri, headers=headers, content=body)

        resp.raise_for_status()
        return self.parse_response(resp.text)
