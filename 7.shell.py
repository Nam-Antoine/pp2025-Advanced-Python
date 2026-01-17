"""
Python Shell - Execute system commands with I/O redirection and piping support
"""

import subprocess
import sys
import os
import platform

class Shell:
    def __init__(self):
        self.running = True
        self.is_windows = platform.system() == "Windows"
        
        # Command aliases for Windows
        self.aliases = {
            'ls': 'dir',
            'cat': 'type',
            'grep': 'findstr',
            'ps': 'tasklist',
            'pwd': 'cd',
            'rm': 'del',
            'mv': 'move',
            'cp': 'copy',
            'clear': 'cls',
        } if self.is_windows else {}
    
    def translate_command(self, cmd_list):
        """Translate Unix commands to Windows equivalents if needed"""
        if not cmd_list:
            return cmd_list
        
        if self.is_windows and cmd_list[0] in self.aliases:
            cmd_list[0] = self.aliases[cmd_list[0]]
        
        return cmd_list
    
    def parse_command(self, line):
        """Parse command line into tokens, handling redirection and pipes"""
        tokens = line.split()
        command_parts = []
        input_file = None
        output_file = None
        pipes = []
        current_command = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Handle input redirection
            if token == '<':
                if i + 1 < len(tokens):
                    input_file = tokens[i + 1]
                    i += 2
                    continue
            
            # Handle output redirection
            elif token == '>':
                if i + 1 < len(tokens):
                    output_file = tokens[i + 1]
                    i += 2
                    continue
            
            # Handle pipe
            elif token == '|':
                if current_command:
                    pipes.append(current_command)
                    current_command = []
                i += 1
                continue
            
            else:
                current_command.append(token)
            
            i += 1
        
        # Add the last command
        if current_command:
            pipes.append(current_command)
        
        return pipes, input_file, output_file
    
    def execute_command(self, pipes, input_file, output_file):
        """Execute command(s) with piping and redirection"""
        try:
            # Prepare input
            stdin_data = None
            if input_file:
                if not os.path.exists(input_file):
                    print(f"Error: Input file '{input_file}' not found")
                    return
                with open(input_file, 'r') as f:
                    stdin_data = f.read()
            
            # Execute piped commands
            process = None
            for i, cmd in enumerate(pipes):
                # Translate commands for Windows
                cmd = self.translate_command(cmd)
                
                stdin = subprocess.PIPE if i == 0 else (process.stdout if process else None)
                stdout = subprocess.PIPE if i < len(pipes) - 1 or output_file else sys.stdout
                
                process = subprocess.Popen(
                    cmd,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=self.is_windows  # Use shell on Windows for better command support
                )
                
                if i == 0 and stdin_data:
                    process.stdin.write(stdin_data)
                    process.stdin.close()
            
            # Handle output redirection
            if output_file:
                with open(output_file, 'w') as f:
                    if process:
                        stdout, stderr = process.communicate()
                        if stdout:
                            f.write(stdout)
                        if stderr:
                            print(stderr, file=sys.stderr)
                print(f"Output redirected to '{output_file}'")
            else:
                if process:
                    stdout, stderr = process.communicate()
                    if stdout:
                        print(stdout, end='')
                    if stderr:
                        print(stderr, file=sys.stderr, end='')
        
        except FileNotFoundError as e:
            print(f"Command not found: {e}")
        except Exception as e:
            print(f"Error executing command: {e}")
    
    def run(self):
        """Main shell loop"""
        print("=" * 50)
        print(f"Python Shell - {platform.system()} Mode")
        print("Unix commands will be translated to Windows equivalents")
        print("Type 'exit' to quit, 'help' for commands")
        print("=" * 50)
        
        while self.running:
            try:
                # Display prompt
                prompt = f"{os.getcwd()}$ "
                user_input = input(prompt).strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle exit command
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    self.running = False
                    break
                
                # Handle help command
                if user_input.lower() == 'help':
                    print("\nCommand Aliases (Unix -> Windows):")
                    for unix_cmd, win_cmd in self.aliases.items():
                        print(f"  {unix_cmd:10} -> {win_cmd}")
                    print("\nFeatures:")
                    print("  - I/O Redirection: < (input), > (output)")
                    print("  - Piping: | (pipe between commands)")
                    print("  - Directory: cd <path>")
                    print()
                    continue
                
                # Handle cd command (change directory)
                if user_input.startswith('cd '):
                    path = user_input[3:].strip()
                    try:
                        os.chdir(path)
                    except FileNotFoundError:
                        print(f"Directory not found: {path}")
                    continue
                
                # Parse and execute command
                pipes, input_file, output_file = self.parse_command(user_input)
                
                if pipes:
                    self.execute_command(pipes, input_file, output_file)
            
            except KeyboardInterrupt:
                print("\n")
                continue
            except Exception as e:
                print(f"Error: {e}")


def main():
    shell = Shell()
    shell.run()


if __name__ == "__main__":
    main()
