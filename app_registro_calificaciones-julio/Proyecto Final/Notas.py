class Notas:
  
  def __init__(self, list):
    self.set_ppractica(list[0])
    self.set_spractica(list[1])
    self.set_pforo(list[2])
    self.set_sforo(list[3])
    self.set_pparcial(list[4])
    self.set_sparcial(list[5])
    self.set_final(list[6])
  #end ctr

  def set_ppractica(self, value):
    self._ppractica = value
  #end method

  def set_spractica(self, value):
    self._spractica = value
  #end method

  def set_pforo(self, value):
    self._pforo = value
  #end method

  def set_sforo(self, value):
    self._sforo = value
  #end method

  def set_pparcial(self, value):
    self._pparcial = value
  #end method

  def set_sparcial(self, value):
    self._sparcial = value
  #end method

  def set_final(self, value):
    self._final = value
  #end method

  #getters
  def get_ppractica(self):
    return self._ppractica
  #end method

  def get_spractica(self):
    return self._spractica
  #end method

  def get_pforo(self):
    return self._pforo
  #end method

  def get_sforo(self):
    return self._sforo
  #end method

  def get_pparcial(self):
    return self._pparcial
  #end method

  def get_sparcial(self):
    return self._sparcial
  #end method

  def get_final(self):
    return self._final
  #end method

  def is_valid(self):
    valido = True
    if self.get_ppractica()==''or int(self.get_ppractica()) < 0 or int(self.get_ppractica()) > 100:
      valido=False
    if self.get_spractica()=='' or int(self.get_spractica()) < 0 or int(self.get_spractica()) > 100:
      valido=False
    if self.get_pforo()=='' or int(self.get_pforo()) < 0 or int(self.get_pforo()) > 100:
      valido=False
    if self.get_sforo()=='' or int(self.get_sforo()) < 0 or int(self.get_sforo()) > 100:
      valido=False
    if self.get_pparcial()=='' or int(self.get_pparcial()) < 0 or int(self.get_pparcial()) > 100:
      valido=False
    if self.get_sparcial()=='' or int(self.get_sparcial()) < 0 or int(self.get_sparcial()) > 100:
      valido=False
    if self.get_final()=='' or int(self.get_final()) < 0 or int(self.get_final()) > 100:
      valido=False
    return valido
  #end method
  
#end class