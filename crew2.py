from json import tool

from dotenv import load_dotenv
from crewai import Agent,Task,Crew,Process,LLM
from crewai.project import agent,task,crew,CrewBase

load_dotenv()
llm = LLM(
    model = 'gemini/gemini-3.5-flash-lite',
    temperature = 0.7
)
@CrewBase
class Refactor:
    agents_config = "configuration/agents.yaml"
    tasks_config = "configuration/task.yaml"

    @agent
    def variable_agent(self) -> Agent:
        return Agent(
        config = self.agents_config["Variable_naming_agent"],
        verbose = True,
        llm = llm
        )
    @agent
    def error_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["Error_fixing_agent"],
            verbose=True,
            llm=llm
        )
    @agent
    def description_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["Description_agent"],
            verbose=True,
            llm=llm
        )
    @task
    def variable_task(self) -> Task:
        return Task(
            config = self.tasks_config["Variable_assigning_task"],
            agent = self.variable_agent()
        )
    @task
    def error_task(self) -> Task:
        return Task(
            config = self.tasks_config["Error_fixing_task"],
            agent = self.error_agent()

        )
    @task
    def description_task(self) -> Task:
        return Task(
            config = self.tasks_config["Description_task"],
            agent = self.description_agent()
        )

    @crew
    def crew(self)->Crew:
        return Crew(
          agents=self.agents,
          tasks=self.tasks,
          process = Process.sequential,
          verbose=True
        )

if __name__ == '__main__':
    refactor_crew=Refactor()
    code="""
    class Car:
    def __init__(self, brand, color)  # SyntaxError: invalid syntax (missing colon here)
        self.brand = brand
        self.color = color

    def drive(self):
        print(f"The {self.color} {self.brand} is driving.")

    my_car = Car("Toyota", "red")
    my_car.drive()
    """
    result = refactor_crew.crew().kickoff(inputs={"code":code})
    print(result)

