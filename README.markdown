
<action> <area>

    Städa <gemensam yta>
    
    Städa <egen yta>
    
    Skura <yta>

<action> <one of several options>
    
    Diska
    
    Tvätta [kläder|fönster]
    
    Ta ut [sopor|kompost]
    
<action> <thing>

    Handla {sak}
    
    Reparera {sak}

TaskAction TaskObject
action [area|thing|one-of]


TaskAction

 - name

TaskObject = {
  'type': area or thing or oneof,
  'options': [String] or [],
  'owner': User or None
}
