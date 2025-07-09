import CreateExpenseForm from "../components/CreateExpenseForm";
import ExpenseList from "../components/ExpenseList";
import LogoutButton from "../components/LogoutButton";

function Dashboard () {
    return (
        <div className="p-6">
            <h2 className="text-3xl font-bold">Dashboard</h2>
            <p className="mt-4">Welcome! You’re logged in 🎉</p>

            <CreateExpenseForm/>
            <ExpenseList/>
            <LogoutButton/>
        </div>
    );
}

export default Dashboard;