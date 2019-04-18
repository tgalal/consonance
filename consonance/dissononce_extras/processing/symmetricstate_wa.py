from dissononce.processing.impl.symmetricstate import SymmetricState


class WASymmetricState(SymmetricState):
    """WA does not mix_hash if cipherstate does not yet have a key, therefore this custom WASymmetricState has to
    be used instead of default one."""
    def encrypt_and_hash(self, plaintext):
        ciphertext = self._cipherstate.encrypt_with_ad(self._h, plaintext)
        if self._cipherstate.has_key():
            self.mix_hash(ciphertext)
        return ciphertext
