"""
LANGHAM Hotel Management System
File: langham_hotel_management.py
Author: [Your Name]
Description: Console-based Hotel Management System for LANGHAM Hotels
Date: June 2025
Version: 1.0
"""

import os
import datetime
import json

class LanghamHotelSystem:
    def __init__(self):
        """Initialize the hotel management system with empty room lists"""
        self.rooms = []  # List to store room details
        self.allocated_rooms = []  # List to store allocated room details
        self.student_id = "12345"  # Replace with your actual student ID
        
    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "="*50)
        print("    LANGHAM HOTEL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Room")
        print("2. Delete Room")
        print("3. Display Room Details")
        print("4. Allocate Room")
        print("5. Display Room Allocation Details")
        print("6. Billing & De-Allocation")
        print("7. Save Room Allocation to File")
        print("8. Display Room Allocation from File")
        print("9. Backup and Clear Room Allocation File")
        print("0. Exit Application")
        print("="*50)
        
    def add_room(self):
        """Add new room(s) to the hotel system"""
        try:
            print("\n--- ADD ROOM ---")
            room_number = input("Enter room number: ").strip()
            
            # Check if room already exists
            if any(room['number'] == room_number for room in self.rooms):
                raise ValueError(f"Room {room_number} already exists!")
            
            room_type = input("Enter room type (Single/Double/Suite): ").strip()
            if room_type not in ['Single', 'Double', 'Suite']:
                raise ValueError("Invalid room type! Please enter Single, Double, or Suite.")
            
            price_str = input("Enter room price per night: ").strip()
            if not price_str:
                raise ValueError("Price cannot be empty!")
            
            price = float(price_str)
            if price <= 0:
                raise ValueError("Price must be greater than 0!")
            
            capacity_str = input("Enter room capacity: ").strip()
            if not capacity_str:
                raise ValueError("Capacity cannot be empty!")
            
            capacity = int(capacity_str)
            if capacity <= 0:
                raise ValueError("Capacity must be greater than 0!")
            
            room = {
                'number': room_number,
                'type': room_type,
                'price': price,
                'capacity': capacity,
                'status': 'Available'
            }
            
            self.rooms.append(room)
            print(f"Room {room_number} added successfully!")
            
        except ValueError as e:
            print(f"Value Error: {e}")
        except TypeError as e:
            print(f"Type Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def delete_room(self):
        """Delete room(s) from the hotel system"""
        try:
            if not self.rooms:
                print("No rooms available to delete!")
                return
            
            print("\n--- DELETE ROOM ---")
            room_number = input("Enter room number to delete: ").strip()
            
            # Find and remove the room
            for i, room in enumerate(self.rooms):
                if room['number'] == room_number:
                    if room['status'] == 'Occupied':
                        raise ValueError("Cannot delete occupied room! Please de-allocate first.")
                    
                    del self.rooms[i]
                    print(f"Room {room_number} deleted successfully!")
                    return
            
            raise ValueError(f"Room {room_number} not found!")
            
        except ValueError as e:
            print(f"Value Error: {e}")
        except IndexError as e:
            print(f"Index Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def display_rooms(self):
        """Display all room details"""
        try:
            print("\n--- ROOM DETAILS ---")
            
            if not self.rooms:
                print("No rooms available!")
                return
            
            print(f"{'Room No':<10} {'Type':<10} {'Price':<10} {'Capacity':<10} {'Status':<10}")
            print("-" * 50)
            
            for room in self.rooms:
                print(f"{room['number']:<10} {room['type']:<10} ${room['price']:<9.2f} {room['capacity']:<10} {room['status']:<10}")
                
        except Exception as e:
            print(f"Error displaying rooms: {e}")
    
    def allocate_room(self):
        """Allocate room to a customer"""
        try:
            if not self.rooms:
                print("No rooms available for allocation!")
                return
            
            print("\n--- ALLOCATE ROOM ---")
            
            # Display available rooms
            available_rooms = [room for room in self.rooms if room['status'] == 'Available']
            if not available_rooms:
                print("No rooms available for allocation!")
                return
            
            print("Available Rooms:")
            for room in available_rooms:
                print(f"Room {room['number']} - {room['type']} - ${room['price']}/night")
            
            room_number = input("Enter room number to allocate: ").strip()
            
            # Find the room
            room = None
            for r in self.rooms:
                if r['number'] == room_number:
                    room = r
                    break
            
            if not room:
                raise ValueError(f"Room {room_number} not found!")
            
            if room['status'] != 'Available':
                raise ValueError(f"Room {room_number} is not available!")
            
            customer_name = input("Enter customer name: ").strip()
            if not customer_name:
                raise ValueError("Customer name cannot be empty!")
            
            nights_str = input("Enter number of nights: ").strip()
            if not nights_str:
                raise ValueError("Number of nights cannot be empty!")
            
            nights = int(nights_str)
            if nights <= 0:
                raise ValueError("Number of nights must be greater than 0!")
            
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
            try:
                datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format! Please use YYYY-MM-DD.")
            
            total_cost = room['price'] * nights
            
            allocation = {
                'room_number': room_number,
                'customer_name': customer_name,
                'nights': nights,
                'check_in_date': check_in_date,
                'total_cost': total_cost,
                'allocation_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.allocated_rooms.append(allocation)
            room['status'] = 'Occupied'
            
            print(f"Room {room_number} allocated to {customer_name} successfully!")
            print(f"Total cost: ${total_cost:.2f}")
            
        except ValueError as e:
            print(f"Value Error: {e}")
        except TypeError as e:
            print(f"Type Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def display_allocation_details(self):
        """Display current room allocation status"""
        try:
            print("\n--- ROOM ALLOCATION DETAILS ---")
            
            if not self.allocated_rooms:
                print("No rooms currently allocated!")
                return
            
            print(f"{'Room No':<10} {'Customer':<15} {'Nights':<8} {'Check-in':<12} {'Total Cost':<12}")
            print("-" * 67)
            
            for allocation in self.allocated_rooms:
                print(f"{allocation['room_number']:<10} {allocation['customer_name']:<15} "
                      f"{allocation['nights']:<8} {allocation['check_in_date']:<12} "
                      f"${allocation['total_cost']:<11.2f}")
                
        except Exception as e:
            print(f"Error displaying allocation details: {e}")
    
    def billing_and_deallocation(self):
        """Generate bill and release room"""
        try:
            if not self.allocated_rooms:
                print("No allocated rooms for billing!")
                return
            
            print("\n--- BILLING & DE-ALLOCATION ---")
            room_number = input("Enter room number for billing: ").strip()
            
            # Find allocation
            allocation = None
            allocation_index = -1
            for i, alloc in enumerate(self.allocated_rooms):
                if alloc['room_number'] == room_number:
                    allocation = alloc
                    allocation_index = i
                    break
            
            if not allocation:
                raise ValueError(f"No allocation found for room {room_number}!")
            
            # Generate bill
            print("\n" + "="*40)
            print("           LANGHAM HOTEL BILL")
            print("="*40)
            print(f"Room Number: {allocation['room_number']}")
            print(f"Customer: {allocation['customer_name']}")
            print(f"Check-in Date: {allocation['check_in_date']}")
            print(f"Number of Nights: {allocation['nights']}")
            print(f"Total Amount: ${allocation['total_cost']:.2f}")
            print(f"Bill Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*40)
            print("Thank you for staying with LANGHAM Hotels!")
            print("="*40)
            
            # De-allocate room
            del self.allocated_rooms[allocation_index]
            
            # Update room status
            for room in self.rooms:
                if room['number'] == room_number:
                    room['status'] = 'Available'
                    break
            
            print(f"\nRoom {room_number} has been de-allocated successfully!")
            
        except ValueError as e:
            print(f"Value Error: {e}")
        except IndexError as e:
            print(f"Index Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def save_allocation_to_file(self):
        """Save room allocation data to file"""
        try:
            filename = f"LHMS_{self.student_id}.txt"
            
            with open(filename, 'w') as file:
                file.write("LANGHAM HOTEL MANAGEMENT SYSTEM\n")
                file.write("Room Allocation Report\n")
                file.write("="*50 + "\n")
                file.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if not self.allocated_rooms:
                    file.write("No rooms currently allocated.\n")
                else:
                    file.write(f"{'Room No':<10} {'Customer':<15} {'Nights':<8} {'Check-in':<12} {'Total Cost':<12}\n")
                    file.write("-" * 67 + "\n")
                    
                    for allocation in self.allocated_rooms:
                        file.write(f"{allocation['room_number']:<10} {allocation['customer_name']:<15} "
                                  f"{allocation['nights']:<8} {allocation['check_in_date']:<12} "
                                  f"${allocation['total_cost']:<11.2f}\n")
            
            print(f"Room allocation data saved to {filename} successfully!")
            
        except IOError as e:
            print(f"IO Error: {e}")
        except FileNotFoundError as e:
            print(f"File Not Found Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def display_allocation_from_file(self):
        """Display room allocation data from file"""
        try:
            filename = f"LHMS_{self.student_id}.txt"
            
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} does not exist!")
            
            with open(filename, 'r') as file:
                content = file.read()
                if not content.strip():
                    raise EOFError("File is empty!")
                
                print("\n--- FILE CONTENT ---")
                print(content)
                
        except FileNotFoundError as e:
            print(f"File Not Found Error: {e}")
        except IOError as e:
            print(f"IO Error: {e}")
        except EOFError as e:
            print(f"EOF Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def backup_and_clear_file(self):
        """Backup and clear room allocation file"""
        try:
            filename = f"LHMS_{self.student_id}.txt"
            backup_filename = f"LHMS_{self.student_id}_Backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} does not exist!")
            
            # Read original file content
            with open(filename, 'r') as original_file:
                content = original_file.read()
                if not content.strip():
                    print("Original file is empty, nothing to backup.")
                    return
            
            # Create backup file
            with open(backup_filename, 'w') as backup_file:
                backup_file.write(f"BACKUP CREATED ON: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                backup_file.write("="*50 + "\n")
                backup_file.write(content)
            
            # Clear original file
            with open(filename, 'w') as original_file:
                original_file.write("")
            
            print(f"Backup created: {backup_filename}")
            print(f"Original file {filename} has been cleared.")
            
        except FileNotFoundError as e:
            print(f"File Not Found Error: {e}")
        except IOError as e:
            print(f"IO Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def run(self):
        """Main application loop"""
        print("Welcome to LANGHAM Hotel Management System!")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (0-9): ").strip()
                
                if choice == '1':
                    self.add_room()
                elif choice == '2':
                    self.delete_room()
                elif choice == '3':
                    self.display_rooms()
                elif choice == '4':
                    self.allocate_room()
                elif choice == '5':
                    self.display_allocation_details()
                elif choice == '6':
                    self.billing_and_deallocation()
                elif choice == '7':
                    self.save_allocation_to_file()
                elif choice == '8':
                    self.display_allocation_from_file()
                elif choice == '9':
                    self.backup_and_clear_file()
                elif choice == '0':
                    print("\nThank you for using LANGHAM Hotel Management System!")
                    print("Goodbye!")
                    break
                else:
                    raise ValueError("Invalid choice! Please enter a number between 0-9.")
                    
            except ValueError as e:
                print(f"Input Error: {e}")
            except KeyboardInterrupt:
                print("\n\nApplication interrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"Unexpected Error: {e}")
            
            # Pause for user to read output
            input("\nPress Enter to continue...")

# Entry point for the application
if __name__ == "__main__":
    try:
        hotel_system = LanghamHotelSystem()
        hotel_system.run()
    except ImportError as e:
        print(f"Import Error: {e}")
    except NameError as e:
        print(f"Name Error: {e}")
    except Exception as e:
        print(f"Fatal Error: {e}")