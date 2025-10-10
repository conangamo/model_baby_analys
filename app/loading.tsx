import Image from "next/image";

export default function Loading() {
	return (
		<div className="fixed inset-0 z-50 grid place-items-center bg-background">
			<div className="flex flex-col items-center gap-6">
				<h1 className="text-2xl font-bold">Baby care and support</h1>
				<div className="flex items-center gap-2 text-muted-foreground">
					<span className="sr-only">Loading</span>
					<div className="h-3 w-3 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]"></div>
					<div className="h-3 w-3 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]"></div>
					<div className="h-3 w-3 rounded-full bg-primary animate-bounce"></div>
				</div>
			</div>
		</div>
	);
}


