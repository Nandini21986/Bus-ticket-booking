import hashlib
import time
import streamlit as st

# === Blockchain Classes ===
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.ctime()
        self.data = data  # booking details
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        record = f'{self.index}{self.timestamp}{self.data}{self.previous_hash}'
        return hashlib.sha256(record.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_booking(self, passenger, bus_id):
        booking_data = f"Passenger: {passenger}, Bus ID: {bus_id}"
        previous_hash = self.get_latest_block().hash
        new_block = Block(len(self.chain), booking_data, previous_hash)
        self.chain.append(new_block)

    def display_chain(self):
        for block in self.chain:
            st.markdown(f"### Block {block.index}")
            st.write(f"**Timestamp:** {block.timestamp}")
            st.write(f"**Data:** {block.data}")
            st.write(f"**Hash:** `{block.hash}`")
            st.write(f"**Previous Hash:** `{block.previous_hash}`")
            st.markdown("---")

# === Initialize Blockchain in Session ===
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

# === Streamlit UI ===
st.title("🚌 Bus Booking Blockchain System")

# Input fields
passenger = st.text_input("Passenger Name")
bus_id = st.text_input("Bus ID")

# Booking button
if st.button("Add Booking"):
    if passenger and bus_id:
        st.session_state.blockchain.add_booking(passenger, bus_id)
        st.success(f"Booking added for {passenger} on Bus {bus_id}")
    else:
        st.error("Please provide both passenger name and bus ID.")

# Show blockchain
st.subheader("🔗 Blockchain Ledger")
st.session_state.blockchain.display_chain()
