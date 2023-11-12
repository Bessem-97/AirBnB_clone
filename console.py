#!/usr/bin/python
"""
Module for console
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City



def split_curly_braces(incoming_xtra_arg):
    """
    Splits the curly braces for the update method

    incoming_xtra_arg = '"87f12", "first_name", "John"'

    incoming_xtra_arg = '"87f12", {'first_name': "John", "age": 89}'
    """
    curly_braces = re.search(r"\{(.*?)\}", incoming_xtra_arg)

    if curly_braces:
        id_with_comma = shlex.split(incoming_xtra_arg[:curly_braces.span()[0]])
        # "87f12",
        id = [i.strip(",") for i in id_with_comma][0]

        str_data = curly_braces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return id, arg_dict
    # expected return ("87f12", {'first_name': "John", "age": 89})
    else:
        # expecting '"87f12", "first_name", "John"'
        commands = incoming_xtra_arg.split(",")
        try:
            id = commands[0]
            attr_name = commands[1]
            attr_value = commands[2]
            return f"{id}", f"{attr_name} {attr_value}"
            # expected return ("87f12", "first_name" "John")
        # modified from print("** argument missing **") to pass
        except Exception:
            pass

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity",
                     "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_EOF(self, arg):
        """
        EOF (Ctrl+D) signal to exit the program.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True
        

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{commands[0]}()")
            storage.save()
            print(new_instance.id)

    

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: <User>.all()
                <User>.show()
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))
        
    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class
        usage: <class name>.count()
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if arg:
            incoming_class_name = commands[0]


        count = 0

        if commands:
            if incoming_class_name in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == incoming_class_name:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                curly_braces = re.search(r"\{(.*?)\}", arg)

                if curly_braces:
                    # added to catch errors
                    try:
                        str_data = curly_braces.group(1)

                        arg_dict = ast.literal_eval("{" + str_data + "}")

                        attribute_names = list(arg_dict.keys())
                        attribute_values = list(arg_dict.values())
                        # added to catch exception
                        try:
                            attr_name1 = attribute_names[0]
                            attr_value1 = attribute_values[0]
                            setattr(obj, attr_name1, attr_value1)
                        except Exception:
                            pass
                        try:
                            # added to catch exception
                            attr_name2 = attribute_names[1]
                            attr_value2 = attribute_values[1]
                            setattr(obj, attr_name2, attr_value2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:

                    attr_name = commands[2]
                    attr_value = commands[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()
    
    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
            usage:
                <class_name>.<method><("id", {"attr_name": "attr_value", "attr_name": "attr_value")>

        """
        arg_list = arg.split('.')

        incoming_class_name = arg_list[0]

        command = arg_list[1].split('(')

        incoming_method = command[0]
        
        incoming_xtra_arg = command[1].split(')')[0]
        
        

        method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
                }
        if incoming_method in method_dict.keys():
            if incoming_method != "update":
                return method_dict[incoming_method]("{} {}".format(incoming_class_name,
                                                                   incoming_xtra_arg))
            else:
                try:
                    obj_id, arg_dict = split_curly_braces(incoming_xtra_arg)
                # modified from print("** no instance found **") to pass
                except Exception:
                    pass
                try:
                    if isinstance(arg_dict, str):
                        attributes = arg_dict
                        return method_dict[incoming_method]("{} {} {}".format(incoming_class_name,
                                                                                 obj_id,
                                                                                 attributes))
                    elif isinstance(arg_dict, dict):
                        dict_attributes = arg_dict
                        return method_dict[incoming_method]("{} {} {}".format(incoming_class_name,
                                                                           obj_id,
                                                                           dict_attributes))
                # modified from print("** argument missing **") to pass
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False
    

if __name__ == '__main__':
    HBNBCommand().cmdloop()