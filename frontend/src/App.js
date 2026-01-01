
import { useState, useEffect, useCallback } from "react"; 
import "@/App.css"; 
import axios from "axios"; 
import { Toaster, toast } from "sonner"; 
import { Upload, Play, Trash2, Users, TrendingUp, Mail, Activity, ChevronDown, RefreshCw, FileText, Download, X, AlertCircle, CheckCircle, Clock, Zap, Target, BarChart3, } from "lucide-react"; 
import { Button } from "@/components/ui/button"; 
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"; 
import { Badge } from "@/components/ui/badge"; 
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"; 
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, } from "@/components/ui/table"; 
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger,} from \"@/components/ui/dialog\";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, } from "@/components/ui/dropdown-menu"; 
import { ScrollArea } from "@/components/ui/scroll-area"; 
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger, } from "@/components/ui/tooltip"; 

const API = ${process.env.REACT_APP_BACKEND_URL}/api; 

// Priority Badge Component const PriorityBadge = ({ priority }) => { const styles = { HIGH: "bg-red-500/10 text-red-400 border-red-500/20", MEDIUM: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20", LOW: "bg-blue-500/10 text-blue-400 border-blue-500/20", }; 

return ( <Badge variant="outline" className={${styles[priority] || styles.LOW} font-mono text-xs uppercase tracking-wider} data-testid={priority-badge-${priority?.toLowerCase()}} > {priority} ); }; 

// Score Display Component const ScoreDisplay = ({ score }) => { let colorClass = "text-slate-400"; if (score >= 70) colorClass = "text-emerald-400"; else if (score >= 40) colorClass = "text-yellow-400"; 

return ( <span className={font-mono font-medium ${colorClass}} data-testid="score-display"> {score} ); }; 

// Stats Card Component const StatsCard = ({ title, value, icon: Icon, trend, color = "primary" }) => { const colorStyles = { primary: "from-indigo-500/20 to-transparent", success: "from-emerald-500/20 to-transparent", warning: "from-yellow-500/20 to-transparent", danger: "from-red-500/20 to-transparent", info: "from-cyan-500/20 to-transparent", }; 

return ( <Card className="relative overflow-hidden border-white/5 bg-card" data-testid={stats-card-${title.toLowerCase().replace(/\s/g, '-')}}> <div className={absolute top-0 right-0 w-32 h-32 bg-gradient-radial ${colorStyles[color]} blur-2xl} /> <CardContent className="p-6"> <div className="flex items-center justify-between">  

<p className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-1"> {title}  

<p className="text-3xl font-bold font-mono">{value} 

{trend && ( <p className="text-xs text-muted-foreground mt-1">{trend} 

)}  

<div className="p-3 rounded-lg bg-white/5"> <Icon className="h-6 w-6 text-muted-foreground" strokeWidth={1.5} /> ); }; 

// Score Breakdown Tooltip const ScoreBreakdown = ({ breakdown }) => { if (!breakdown || breakdown.length === 0) return null; 

return ( <div className="space-y-2 p-2"> <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground mb-2"> Score Breakdown  

{breakdown.map((item, idx) => ( <div key={idx} className="flex justify-between text-sm"> <span className="text-muted-foreground">{item.category} <span className="font-mono text-foreground">+{item.points} ))} ); }; 

// Activity Log Item const ActivityLogItem = ({ log }) => { const icons = { lead_scored: Target, email_sent: Mail, csv_upload: Upload, leads_processed: Zap, }; const Icon = icons[log.event_type] || Activity; 

const statusColors = { success: "text-emerald-400", error: "text-red-400", warning: "text-yellow-400", }; 

const formatTime = (timestamp) => { const date = new Date(timestamp); return date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", }); }; 

return ( <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors" data-testid="activity-log-item"> <div className="p-2 rounded-md bg-white/5"> <Icon className={h-4 w-4 ${statusColors[log.status] || 'text-muted-foreground'}} strokeWidth={1.5} /> <div className="flex-1 min-w-0"> <p className="text-sm font-medium truncate"> {log.event_type.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}  

<p className="text-xs text-muted-foreground truncate"> {log.data?.lead_name || log.data?.filename || ${log.data?.total_leads || 0} leads}  

<span className="text-xs text-muted-foreground font-mono"> {formatTime(log.timestamp)} ); }; 

// CSV Upload Dialog const CSVUploadDialog = ({ onUpload, isLoading }) => { const [dragActive, setDragActive] = useState(false); const [selectedFile, setSelectedFile] = useState(null); 

const handleDrag = (e) => { e.preventDefault(); e.stopPropagation(); if (e.type === "dragenter" || e.type === "dragover") { setDragActive(true); } else if (e.type === "dragleave") { setDragActive(false); } }; 

const handleDrop = (e) => { e.preventDefault(); e.stopPropagation(); setDragActive(false); if (e.dataTransfer.files && e.dataTransfer.files[0]) { setSelectedFile(e.dataTransfer.files[0]); } }; 

const handleFileSelect = (e) => { if (e.target.files && e.target.files[0]) { setSelectedFile(e.target.files[0]); } }; 

const handleUpload = () => { if (selectedFile) { onUpload(selectedFile); setSelectedFile(null); } }; 

return ( <Button className="btn-lift" data-testid="upload-csv-btn"> <Upload className="mr-2 h-4 w-4" /> Upload CSV <DialogContent className=\"sm:max-w-md bg-card border-white/10\"><DialogHeader><DialogTitle> Upload Leads CSV </DialogTitle><DialogDescription>  CSV <div className={relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${ dragActive ? \"border-primary bg-primary/5\" : \"border-white/10 hover:border-white/20\" }} onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop} data-testid="csv-drop-zone" > <input type="file" accept=".csv" onChange={handleFileSelect} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" data-testid="csv-file-input" /> <FileText className="mx-auto h-12 w-12 text-muted-foreground mb-4" /> <p className="text-sm text-muted-foreground mb-1"> Drag and drop your CSV file here, or click to browse  

<p className="text-xs text-muted-foreground"> Required: name, email, company, company_size, industry, budget  

  {selectedFile && ( 
     <div className=\"flex items-center justify-between p-3 bg-white/5 rounded-lg\"> 
       <div className=\"flex items-center gap-2\"> 
         <FileText className=\"h-4 w-4 text-primary\" /> 
         <span className=\"text-sm truncate\">{selectedFile.name}</span> 
       </div> 
       <Button 
         variant=\"ghost\" 
         size=\"icon\" 
         onClick={() => setSelectedFile(null)} 
         data-testid=\"remove-file-btn\" 
       > 
         <X className=\"h-4 w-4\" /> 
       </Button> 
     </div> 
   )} 
 
   <div className=\"flex justify-end gap-2\"> 
     <Button 
       onClick={handleUpload} 
       disabled={!selectedFile || isLoading} 
       className=\"btn-lift\" 
       data-testid=\"confirm-upload-btn\" 
     > 
       {isLoading ? ( 
         <RefreshCw className=\"mr-2 h-4 w-4 animate-spin\" /> 
       ) : ( 
         <Upload className=\"mr-2 h-4 w-4\" /> 
       )} 
       Upload 
     </Button> 
   </div> 
 </DialogContent> 
</Dialog> 
 

); }; 

// Main Dashboard Component function App() { const [leads, setLeads] = useState([]); const [logs, setLogs] = useState([]); const [stats, setStats] = useState({ total_leads: 0, high_priority: 0, medium_priority: 0, low_priority: 0, emails_sent: 0, average_score: 0, }); const [isLoading, setIsLoading] = useState(false); const [activeTab, setActiveTab] = useState("leads"); 

const fetchLeads = useCallback(async () => { try { const response = await axios.get(${API}/leads); setLeads(response.data); } catch (error) { console.error("Error fetching leads:", error); toast.error("Failed to fetch leads"); } }, []); 

const fetchStats = useCallback(async () => { try { const response = await axios.get(${API}/leads/stats); setStats(response.data); } catch (error) { console.error("Error fetching stats:", error); } }, []); 

const fetchLogs = useCallback(async () => { try { const response = await axios.get(${API}/logs?limit=50); setLogs(response.data); } catch (error) { console.error("Error fetching logs:", error); } }, []); 

const refreshData = useCallback(async () => { await Promise.all([fetchLeads(), fetchStats(), fetchLogs()]); }, [fetchLeads, fetchStats, fetchLogs]); 

useEffect(() => { refreshData(); }, [refreshData]); 

const handleUploadCSV = async (file) => { setIsLoading(true); const formData = new FormData(); formData.append("file", file); 

try { 
 const response = await axios.post(`${API}/leads/upload`, formData, { 
   headers: { \"Content-Type\": \"multipart/form-data\" }, 
 }); 
 toast.success(response.data.message); 
 await refreshData(); 
} catch (error) { 
 const msg = error.response?.data?.detail || \"Failed to upload CSV\"; 
 toast.error(msg); 
} finally { 
 setIsLoading(false); 
} 
 

}; 

const handleProcessLeads = async () => { setIsLoading(true); try { const response = await axios.post(${API}/leads/process); toast.success( Processed ${response.data.total_leads} leads. ${response.data.emails_sent} emails sent (mock). ); await refreshData(); } catch (error) { toast.error("Failed to process leads"); } finally { setIsLoading(false); } }; 

const handleDeleteLead = async (leadId) => { try { await axios.delete(${API}/leads/${leadId}); toast.success("Lead deleted"); await refreshData(); } catch (error) { toast.error("Failed to delete lead"); } }; 

const handleClearAllLeads = async () => { if (!window.confirm("Are you sure you want to delete all leads?")) return; try { await axios.delete(${API}/leads); toast.success("All leads deleted"); await refreshData(); } catch (error) { toast.error("Failed to delete leads"); } }; 

const handleClearLogs = async () => { try { await axios.delete(${API}/logs); toast.success("Logs cleared"); await fetchLogs(); } catch (error) { toast.error("Failed to clear logs"); } }; 

const handleDownloadSampleCSV = async () => { try { const response = await axios.get(${API}/sample-csv); const blob = new Blob([response.data.csv_content], { type: "text/csv" }); const url = window.URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "sample_leads.csv"; a.click(); window.URL.revokeObjectURL(url); toast.success("Sample CSV downloaded"); } catch (error) { toast.error("Failed to download sample CSV"); } }; 

return ( <div className="min-h-screen bg-background noise-overlay" data-testid="easyfinder-dashboard"> <Toaster position="top-right" theme="dark" richColors /> 

  {/* Header */} 
   <header className=\"sticky top-0 z-40 glass border-b border-white/5\"> 
     <div className=\"max-w-[1800px] mx-auto px-4 md:px-8 py-4\"> 
       <div className=\"flex items-center justify-between\"> 
         <div className=\"flex items-center gap-4\"> 
           <div className=\"flex items-center gap-3\"> 
             <div className=\"w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white\"> 
               EF 
             </div> 
             <div> 
               <h1 className=\"text-xl font-bold tracking-tight\">EasyFinder AI</h1> 
               <p className=\"text-xs text-muted-foreground font-mono uppercase tracking-widest\"> 
                 Lead Management 
               </p> 
             </div> 
           </div> 
         </div> 
 
         <div className=\"flex items-center gap-3\"> 
           <Button 
             variant=\"outline\" 
             size=\"sm\" 
             onClick={handleDownloadSampleCSV} 
             className=\"hidden sm:flex\" 
             data-testid=\"download-sample-btn\" 
           > 
             <Download className=\"mr-2 h-4 w-4\" /> 
             Sample CSV 
           </Button> 
           <CSVUploadDialog onUpload={handleUploadCSV} isLoading={isLoading} /> 
           <Button 
             onClick={handleProcessLeads} 
             disabled={isLoading || leads.length === 0} 
             className=\"btn-lift bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500\" 
             data-testid=\"process-leads-btn\" 
           > 
             {isLoading ? ( 
               <RefreshCw className=\"mr-2 h-4 w-4 animate-spin\" /> 
             ) : ( 
               <Play className=\"mr-2 h-4 w-4\" /> 
             )} 
             Process Leads 
           </Button> 
         </div> 
       </div> 
     </div> 
   </header> 
 
   {/* Main Content */} 
   <main className=\"max-w-[1800px] mx-auto px-4 md:px-8 py-6\"> 
     {/* Stats Grid */} 
     <div className=\"grid grid-cols-2 md:grid-cols-4 gap-4 mb-6\"> 
       <StatsCard 
         title=\"Total Leads\" 
         value={stats.total_leads} 
         icon={Users} 
         color=\"primary\" 
       /> 
       <StatsCard 
         title=\"High Priority\" 
         value={stats.high_priority} 
         icon={TrendingUp} 
         color=\"danger\" 
       /> 
       <StatsCard 
         title=\"Avg Score\" 
         value={stats.average_score} 
         icon={BarChart3} 
         color=\"info\" 
       /> 
       <StatsCard 
         title=\"Emails Sent\" 
         value={stats.emails_sent} 
         icon={Mail} 
         color=\"success\" 
         trend=\"Mock mode\" 
       /> 
     </div> 
 
     {/* Main Grid */} 
     <div className=\"grid grid-cols-1 lg:grid-cols-4 gap-6\"> 
       {/* Leads Table */} 
       <div className=\"lg:col-span-3\"> 
         <Card className=\"border-white/5 bg-card\"> 
           <CardHeader className=\"border-b border-white/5 pb-4\"> 
             <div className=\"flex items-center justify-between\"> 
               <CardTitle className=\"text-lg font-semibold\">Leads</CardTitle> 
               <div className=\"flex items-center gap-2\"> 
                 <Button 
                   variant=\"ghost\" 
                   size=\"sm\" 
                   onClick={refreshData} 
                   data-testid=\"refresh-btn\" 
                 > 
                   <RefreshCw className=\"h-4 w-4\" /> 
                 </Button> 
                 <DropdownMenu> 
                   <DropdownMenuTrigger asChild> 
                     <Button variant=\"outline\" size=\"sm\" data-testid=\"leads-actions-dropdown\"> 
                       Actions <ChevronDown className=\"ml-1 h-4 w-4\" /> 
                     </Button> 
                   </DropdownMenuTrigger> 
                   <DropdownMenuContent align=\"end\" className=\"bg-card border-white/10\"> 
                     <DropdownMenuItem 
                       onClick={handleClearAllLeads} 
                       className=\"text-red-400 focus:text-red-400\" 
                       data-testid=\"clear-all-leads-btn\" 
                     > 
                       <Trash2 className=\"mr-2 h-4 w-4\" /> 
                       Clear All Leads 
                     </DropdownMenuItem> 
                   </DropdownMenuContent> 
                 </DropdownMenu> 
               </div> 
             </div> 
           </CardHeader> 
           <CardContent className=\"p-0\"> 
             {leads.length === 0 ? ( 
               <div className=\"flex flex-col items-center justify-center py-16 text-center\" data-testid=\"empty-leads-state\"> 
                 <Users className=\"h-12 w-12 text-muted-foreground mb-4\" /> 
                 <p className=\"text-muted-foreground mb-2\">No leads yet</p> 
                 <p className=\"text-xs text-muted-foreground mb-4\"> 
                   Upload a CSV file to get started 
                 </p> 
                 <Button 
                   variant=\"outline\" 
                   size=\"sm\" 
                   onClick={handleDownloadSampleCSV} 
                   data-testid=\"empty-state-download-btn\" 
                 > 
                   <Download className=\"mr-2 h-4 w-4\" /> 
                   Download Sample CSV 
                 </Button> 
               </div> 
             ) : ( 
               <ScrollArea className=\"h-[500px]\"> 
                 <Table> 
                   <TableHeader> 
                     <TableRow className=\"hover:bg-transparent border-white/5\"> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground\"> 
                         Name 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground\"> 
                         Company 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground\"> 
                         Industry 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground\"> 
                         Budget 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground text-center\"> 
                         Score 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground text-center\"> 
                         Priority 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground text-center\"> 
                         Email 
                       </TableHead> 
                       <TableHead className=\"text-xs font-mono uppercase tracking-widest text-muted-foreground text-right\"> 
                         Actions 
                       </TableHead> 
                     </TableRow> 
                   </TableHeader> 
                   <TableBody> 
                     {leads.map((lead) => ( 
                       <TableRow 
                         key={lead.id || lead.email} 
                         className=\"table-row-hover border-white/5\" 
                         data-testid={`lead-row-${lead.email}`} 
                       > 
                         <TableCell> 
                           <div> 
                             <p className=\"font-medium\">{lead.name}</p> 
                             <p className=\"text-xs text-muted-foreground\"> 
                               {lead.email} 
                             </p> 
                           </div> 
                         </TableCell> 
                         <TableCell> 
                           <div> 
                             <p className=\"text-sm\">{lead.company}</p> 
                             <p className=\"text-xs text-muted-foreground capitalize\"> 
                               {lead.company_size} 
                             </p> 
                           </div> 
                         </TableCell> 
                         <TableCell className=\"capitalize text-sm\"> 
                           {lead.industry} 
                         </TableCell> 
                         <TableCell className=\"font-mono text-sm\"> 
                           ${parseInt(lead.budget || 0).toLocaleString()} 
                         </TableCell> 
                         <TableCell className=\"text-center\"> 
                           <Tooltip> 
                             <TooltipTrigger> 
                               <ScoreDisplay score={lead.score || 0} /> 
                             </TooltipTrigger> 
                             <TooltipContent side=\"left\" className=\"bg-card border-white/10\"> 
                               <ScoreBreakdown breakdown={lead.breakdown} /> 
                             </TooltipContent> 
                           </Tooltip> 
                         </TableCell> 
                         <TableCell className=\"text-center\"> 
                           <PriorityBadge priority={lead.priority || \"LOW\"} /> 
                         </TableCell> 
                         <TableCell className=\"text-center\"> 
                           {lead.email_sent ? ( 
                             <CheckCircle className=\"h-4 w-4 text-emerald-400 mx-auto\" /> 
                           ) : ( 
                             <Clock className=\"h-4 w-4 text-muted-foreground mx-auto\" /> 
                           )} 
                         </TableCell> 
                         <TableCell className=\"text-right\"> 
                           <Button 
                             variant=\"ghost\" 
                             size=\"icon\" 
                             onClick={() => handleDeleteLead(lead.id)} 
                             className=\"h-8 w-8 text-muted-foreground hover:text-red-400\" 
                             data-testid={`delete-lead-${lead.email}`} 
                           > 
                             <Trash2 className=\"h-4 w-4\" /> 
                           </Button> 
                         </TableCell> 
                       </TableRow> 
                     ))} 
                   </TableBody> 
                 </Table> 
               </ScrollArea> 
             )} 
           </CardContent> 
         </Card> 
       </div> 
 
       {/* Activity Logs */} 
       <div className=\"lg:col-span-1\"> 
         <Card className=\"border-white/5 bg-card h-full\"> 
           <CardHeader className=\"border-b border-white/5 pb-4\"> 
             <div className=\"flex items-center justify-between\"> 
               <CardTitle className=\"text-lg font-semibold\">Activity</CardTitle> 
               <Button 
                 variant=\"ghost\" 
                 size=\"sm\" 
                 onClick={handleClearLogs} 
                 className=\"text-muted-foreground hover:text-red-400\" 
                 data-testid=\"clear-logs-btn\" 
               > 
                 <Trash2 className=\"h-4 w-4\" /> 
               </Button> 
             </div> 
           </CardHeader> 
           <CardContent className=\"p-0\"> 
             <ScrollArea className=\"h-[500px]\"> 
               {logs.length === 0 ? ( 
                 <div className=\"flex flex-col items-center justify-center py-12 text-center px-4\" data-testid=\"empty-logs-state\"> 
                   <Activity className=\"h-10 w-10 text-muted-foreground mb-3\" /> 
                   <p className=\"text-sm text-muted-foreground\">No activity yet</p> 
                 </div> 
               ) : ( 
                 <div className=\"p-2 space-y-1\"> 
                   {logs.map((log) => ( 
                     <ActivityLogItem key={log.id} log={log} /> 
                   ))} 
                 </div> 
               )} 
             </ScrollArea> 
           </CardContent> 
         </Card> 
       </div> 
     </div> 
   </main> 
 
   {/* Footer */} 
   <footer className=\"border-t border-white/5 mt-12\"> 
     <div className=\"max-w-[1800px] mx-auto px-4 md:px-8 py-6\"> 
       <div className=\"flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground\"> 
         <p className=\"font-mono text-xs\"> 
           EasyFinder AI v1.0.0 &bull; Enterprise Lead Management 
         </p> 
         <p className=\"font-mono text-xs\"> 
           Email Mode: <span className=\"text-yellow-400\">MOCK</span> (No real emails sent) 
         </p> 
       </div> 
     </div> 
   </footer> 
 </div> 
</TooltipProvider> 
 

); } 

export default App; 
